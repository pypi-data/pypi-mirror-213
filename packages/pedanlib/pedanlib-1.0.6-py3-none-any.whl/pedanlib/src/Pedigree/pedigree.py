import csv
import pandas as pd
import numpy as np
import os
import re
import networkx as nx
from multiprocessing import Pool, cpu_count
from pedanlib import CanRisk


class Pedigree:
    """
    Pedigree class is based on the old format, a DataFrame with the variables:

    _id_ unique id individual
    _f_  0 if there is no father
    _m_  0 if there is no mother
    _proband 1 for proband and 0 for others
    _age_ current age
    _gender_ 1=male, 2=female, 9=unknown
    _ageOnsetBC1_ of the first breast cancer (0 if there is no breast cancer)
    _ageOnsetBC2_ of the second breast cancer (0 if there is no 2nd breast cancer)
    _ageOnsetPA_  of pancreatic cancer (0 if there is no 2nd breast cancer)
    _ageOnsetPR_  of prostate cancer (0 if there is no 2nd breast cancer)
    _ageOnsetOC_  of ovarian cancer (0 if there is no ovarian cancer)
    _genotype_  0 non-carrier, 1 carrier and 2 for unknown genotypes


    Methods:
        - founders
        - parents
        - enum_conf_p
        - enum_geno_p
        - enum_geno_p_par
        - enum_conf
        - enum_geno
        - enum_geno_par
        - enum_conf_pg
        - enum_geno_par_pg

    """
    ped_file = None
    ped = None
    cr = None
    ps = None
    gs = None
    founders_ = None
    basic_header = ['id', 'f', 'm', 'proband', 'age', 'gender',
                'ageOnsetBC1', 'ageOnsetBC2', 'ageOnsetPA',
                'ageOnsetPR', 'ageOnsetOC', 'genotype']

    def __init__(self, pedigree, tv='brca1'):
        """
        :param ped: pedigree
        """
        self.ps = None
        self.gs = None

        if type(pedigree).__name__ == "DataFrame":
            self.ped = pedigree
        else:
            self.ped_file = pedigree
            format_ = self.get_format(pedigree)

            if format_ == "canrisk":
                self.cr = CanRisk(pedigree)
                self.ped = self.cr.to_basic_format(tv)
                if 'name' in self.ped.columns:
                    self.ped.drop('name', inplace=True, axis=1)
            elif format_ == "basic":
                self.ped = self.pedfile(pedigree)
            else:
                raise Exception("Only CanRisk and Basic format are supported !")

            if self.ped is not None:
                self.ped.set_index(self.ped['id'].to_numpy(), inplace=True)

        self.range = range(1, self.n() + 1)
        self.founders_ = self.founders()

    def toid(self, x):
        return self.ped[x].index.to_list()

    @staticmethod
    def pedfile(file_path):
        """

        :param file_path:
        :return:
        """
        with open(file_path, 'rb') as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.readline().decode('utf-8'))
            df = pd.read_csv(file_path, sep=dialect.delimiter)
            df.sort_values(by='id', inplace=True)
        return df

    def get_format(self, ped_file):
        with open(ped_file, 'r') as file:
            line = file.readline()
            m = re.search('(?<=##)CanRisk', line)
            if m is not None:
                return "canrisk"
            elif set(line.replace('\n', '').split(',')) == set(self.basic_header):
                return "basic"
            else:
                return None

    def set_indiv_valus(self, id, target, val):
        df = self.ped.copy()
        df.at[id, target] = val
        return Pedigree(df)

    def to_ped(self, file_path):
        df = self.ped.copy()
        df.drop(['ageOnsetPA', 'ageOnsetPR'], axis=1, inplace=True)
        return df.to_csv(file_path, header=False, sep=' ', index=False)

    def to_freestyle(self):
        """

        :return:
        """

        def gender_matcher(v):
            match v:
                case 1:
                    return 'M'
                case 2:
                    return 'F'

        def c_matcher(v):
            match v:
                case 'ageOnsetBC1':
                    return 'BrCa'
                case 'ageOnsetBC2':
                    return 'BrCa'
                case 'ageOnsetOC':
                    return 'OvCa'
                case 'ageOnsetPA':
                    return 'PanCa'
                case 'ageOnsetPR':
                    return 'ProCa'

        def genotype_matcher(v):
            match v:
                case 0:
                    return 'Neg'
                case 1:
                    return 'Het'
                case 2:
                    return '.'

        def status(x):
            if all(x == 0):
                return 'unaff', 0
            else:
                x = x[x != 0]
                x = x[x == min(x)]  # in case there is a tie between two types of cancer, then the first is chosen !!!
                return c_matcher(x.index[0]), x[0]

        age_onsets = self.ped[[s for s in self.ped.columns if 'ageOnset' in s]]
        aff_status = age_onsets.apply(status, axis=1)
        sex_ = self.ped.gender.apply(gender_matcher)
        aff_ = pd.Series([v for v, _ in aff_status], index=aff_status.index)
        age_ = pd.Series([self.ped.age[i] if aff_status[i][1] == 0 else aff_status[i][1] for i in self.range], index= aff_status.index)
        geno_ = self.ped.genotype.apply(genotype_matcher)

        fs = pd.DataFrame({'PedID': 'ped1', 'IndID': self.ped.id, 'Father': self.ped.f, 'Mother': self.ped.m,
                          'Sex': sex_, 'Age': age_, 'Aff': aff_, 'Proband': self.ped.proband,
                          'Geno': geno_})
        return fs

    def to_canrisk(self, file_name, update={}, version='2.0'):
        """

        Args:
            version: CanRisk version {1.0, 2.0}
            file_name: canrisk file name (*.crk)
            update: a json (dict of dicts) data with top index the ids and second level
            index canrisk parameters.

            { 1 : {'BRCA1' : '0:N',
                   'BRCA2' : '0:P',
                    ...
                  },
              2 : { ...
                    ...
                  }
            }

        Returns:

        """
        cr_header_v01 = {"##FamID": 'xxx0', "Name": "AN", "Target": 0, "IndivID": 0, "FathID": 0, "MothID": 0,
                         "Sex": None, "MZtwin": 0, "Dead": 0, "Age": 0, "Yob": 0, "BC1": 0, "BC2": 0,
                         "OC": 0, "PRO": 0, "PAN": 0, "Ashkn": 0, "BRCA1": '0:0', "BRCA2": '0:0', "PALB2": '0:0',
                         "ATM": '0:0', "CHEK2": '0:0', "RAD51D": '0:0', "RAD51C": '0:0', "BRIP1": '0:0',
                         "ER:PR:HER2:CK14:CK56": '0:0:0:0:0'}
        cr_header_v02 = {"##FamID": 'xxx0', "Name": "AN", "Target": 0, "IndivID": 0, "FathID": 0, "MothID": 0,
                         "Sex": None, "MZtwin": 0, "Dead": 0, "Age": 0, "Yob": 0, "BC1": 0, "BC2": 0,
                         "OC": 0, "PRO": 0, "PAN": 0, "Ashkn": 0, "BRCA1": '0:0', "BRCA2": '0:0', "PALB2": '0:0',
                         "ATM": '0:0', "CHEK2": '0:0', "BARD1": '0:0', "RAD51D": '0:0', "RAD51C": '0:0', "BRIP1": '0:0',
                         "ER:PR:HER2:CK14:CK56": '0:0:0:0:0'}

        def header(v):
            match v:
                case '1.0':
                    return cr_header_v01.copy()
                case '2.0':
                    return cr_header_v02.copy()

        def genotype_matcher(v):
            match v:
                case 0:
                    return '0:N'
                case 1:
                    return '0:P'
                case 2:
                    return '0:0'

        def gender_matcher(v):
            match v:
                case 1:
                    return 'M'
                case 2:
                    return 'F'


        def to_cr(row):
            # basic_header = ['id', 'f', 'm', 'proband', 'age', 'gender', 'ageOnsetBC1',
            #                'ageOnsetBC2', 'ageOnsetPA', 'ageOnsetPR', 'ageOnsetOC', 'genotype']
            cr_header = header(version)
            row_ = cr_header.copy()
            row_['Name'] = 'NA' if not 'name' in row.index else row['name']
            row_['Target'] = row['proband']
            row_['IndivID'] = row['id']
            row_['FathID'] = row['f']
            row_['MothID'] = row['m']
            row_['Age'] = row['age']
            row_['Sex'] = gender_matcher(row['gender'])
            row_['BC1'] = row['ageOnsetBC1']
            row_['BC2'] = row['ageOnsetBC2']
            row_['PAN'] = row['ageOnsetPA']
            row_['PRO'] = row['ageOnsetPR']
            # In the basic format the genotype does not convey the gene name that is being
            # tested. Therefore, by default all genes {BRCA1, BRCA2, PALB2} are set. It can
            # then be updated with 'update' argument.
            # todo: decide on default setting for genetic test, is the test done for one or all genes?
            # (1) default all are tested
            row_['BRCA1'] = row_['BRCA2'] = row_['PALB2'] = genotype_matcher(row['genotype'])
            # (2) ???
            # row_['BRCA1'] = genotype_matcher(row['genotype'])

            # need a list of testes genes per individual:

            if row['id'] in s.index:
                for g in s[row['id']].keys():
                    row_[g] = s[row['id']][g]

            return row_

        s = pd.Series(update, dtype=object)
        df = pd.DataFrame(list(self.ped.apply(to_cr, axis=1)), index=None)
        version_ = "##CanRisk " + version + '\n'
        export_ = version_ + df.to_csv(sep='\t', index=False)
        with open(file_name, 'w') as f:
            f.write(export_)

    def proband(self):
        return self.ped[self.ped.proband == 1].index.to_list()[0]

    def founders(self):
        """
        It tests whether both parents of 'id' are 0.
        :return: list of 1-based ids of founders
        """
        return self.toid(self.ped.apply(lambda x: x['f'] + x['m'] == 0, axis=1))

    def parents_old(self, id):
        # _id = id - 1
        _id = id
        return [tuple(self.ped['f'])[_id], tuple(self.ped['m'])[_id]]

    def parents(self, id):
        """

        :param id: 1-based index
        :return:
        """
        if id in self.founders_:
            return None
        else:
            return [self.ped['f'][id], self.ped['m'][id]]

    def ancestors(self, id):
        """
        :param id: zero-based id
        :return:
        """

        def anc(par):
            if par is None:
                return []
            else:
                return par + anc(self.parents(par[0])) + anc(self.parents(par[1]))

        return np.array(list(set(anc(self.parents(id)))))

    def offsprings(self, id):
        """

        :param id:
        :return:
        """
        return list(set(self.toid(self.ped['f'] == id) + self.toid(self.ped['m'] == id)))

    def descendants(self, id):
        """
        :param id:
        :return:
        """

        def dsc(id_):
            if len(self.offsprings(id_)) == 0:
                return []
            else:
                return [[i] + dsc(i) for i in self.offsprings(id_)]

        return self.flatten(dsc(id))

    def flatten(self, x):
        """
        :param x: a nested list without empty lists.
        :return: a flat list containing all element from the nested list.
        """
        if type(x) is list and len(x) > 1:
            (h, *t) = x
            if type(h) is list:
                return self.flatten(h) + self.flatten(t)
            else:
                return [h] + self.flatten(t)
        elif type(x) is list and len(x) == 1:
            return self.flatten(x[0])
        elif type(x) is list and len(x) == 0:
            return []
        else:
            return [x]

    def non_founders(self):
        return list(set(self.ped.index) - set(self.founders_))

    def graph(self):
        parent_child_rel = self.ped.loc[self.non_founders()][['id', 'm', 'f']]
        parent_child_edges = parent_child_rel.melt(id_vars=['id'])[['id', 'value']].to_records(index=False)
        spouse_edges = self.ped[self.ped.m != 0][['m', 'f']].drop_duplicates().to_records(index=False)
        edges = list(parent_child_edges) + list(spouse_edges)
        g = nx.Graph()
        g.add_edges_from(edges)
        return g

    def shortest_path(self, i, j):
        return np.array(list(set(nx.shortest_path(self.graph(), i, j))))

    def reachable_founders(self, id):
        return list(set(self.ancestors(id)).intersection(set(self.founders_)))

    def observed(self, value=False):
        if value:
            return self.ped.genotype[self.ped.genotype != 2]
        else:
            return self.ped.genotype != 2

    def n(self, observed=False):
        if not observed:
            return len(self.ped)
        else:
            return sum(self.observed())

    def configurations(self):

        def M():
            def mm_(founder_):
                mm = pd.Series(np.zeros(self.n() + 1), dtype=int)  # take +1 larger vector
                sp = self.shortest_path(self.proband(), founder_)
                dc = self.descendants(founder_)
                mm.loc[sp] = 1
                mm.loc[list(set(dc).difference(set([self.proband()]).union(set(sp))))] = -1
                return mm[1:]  # remove index 0

            return [mm_(founder) for founder in self.reachable_founders(self.proband())]

        def H(x):
            def parents_known_genotype(i):
                parents_ = self.parents(i)
                if parents_ is None:
                    return False
                else:
                    return not (x[parents_] < 0).any()

            # 1)
            hh = pd.Series([2 if (parents_known_genotype(i) & (v < 0)) else v for i, v in x.items()], index=x.index)
            # 2)
            while hh.isin([-1]).any():
                for i in hh.index:
                    if hh[i] < 0:
                        parents_ = self.parents(i)
                        if parents_ is not None:
                            max_ = max(hh[parents_])
                            if max_ > 1:
                                hh[i] = max_ + 1

            return hh

        return [H(s) for s in M()]


    """
    """

    def aff_carrier_stats(self, id):
        p1 = self.set_indiv_valus(id=id, target='ageOnsetBC1', val=81).set_indiv_valus(id=id, target='genotype', val=1)
        p2 = self.set_indiv_valus(id=id, target='ageOnsetBC1', val=81).set_indiv_valus(id=id, target='genotype', val=0)
        p3 = self.set_indiv_valus(id=id, target='age', val=81).set_indiv_valus(id=id, target='genotype', val=1)
        p4 = self.set_indiv_valus(id=id, target='age', val=81).set_indiv_valus(id=id, target='genotype', val=0)
        return [p1, p2, p3, p4]



    """ =================================================================
    enum_geno_par_pg and enum_conf_pg
    x => (p,x)    
    ================================================================= """

    def enum_conf_pg(self, x):
        """
        :param x: is a list of integers, representing the generations
        :return:
        """

        if max(x) > 1:
            idxs = x[x > 1].index
            for i in idxs:
                parents_ = self.parents(i)
                if parents_ is not None:
                    cond = sum(x[parents_])
                else:
                    cond = 0

                if cond == 0:
                    x[i] = 0
                    return self.enum_conf_pg(x)
                elif cond == 1:
                    x0 = x.copy()
                    x0[i] = 0
                    x1 = x.copy()
                    x1[i] = 1
                    return self.enum_conf_pg(x1) + self.enum_conf_pg(x0)
                else:
                    # It may happen that parents also have 'open' genotypes leading to cond > 1
                    # in that case the next index in 'idxs' is taken.
                    continue
        else:
            pp = [self.parents(i) for i in x.index]
            p_ = sum([x[p[0]] + x[p[1]] if p is not None else 0 for p in pp])
            return [(p_, [x])]

    def enum_conf_pg_off(self, x):
        """
        :param x: is a list of integers, representing the generations
        :return:
        """
        stack = [x]
        while len(stack)>0:
            curr = stack.pop()
            for h in curr.max():
                for i in self.range:
                    parents_ = self.parents(i)
                    if parents_ is not None:
                        cond = sum(curr[parents_])
                    else:
                        cond = 0

                    """ 
                    `cond` can take values 0..m: 
                        0: set G_i=0    
                        1: one parent is carrier (two is impossible), split with {G_i=0, G_i=1} 
                        2: means warning if it is 1+1 (impossible case), or one of the parents has 
                        open genotype
                        >2: parents have open genotype 
                    """
                    if cond == 0:
                        curr[i] = 0
                    elif cond == 1:
                        x0 = x.copy()
                        x[i] = 0
                        x0[i] = 1


            else:
                pp = [self.parents(i) for i in x.index]
                p_ = sum([x[p[0]] + x[p[1]] if p is not None else 0 for p in pp])
            return [(p_, [x])]

    def enum_geno_par_pg(self):
        """
        _pg stands for combined p and genotype. The current p and genotype are almost identical except
        :return:
        """

        confs = self.configurations()

        #with Pool(cpu_count()) as p:
        #    gens_ = [g for g in p.map(self.enum_conf_pg, confs)]

        if os.name == 'posix':
            with Pool(cpu_count()) as p:
                gens_ = [g for g in p.map(self.enum_conf_pg, confs)]
        else:
            gens_ = [self.enum_conf_pg(conf) for conf in confs]

        # gens_ = [self.enum_conf_pg(conf) for conf in confs]

        self.ps = [pow(0.5, p_) for c in gens_ for (p_, [x]) in c]
        self.gs = pd.DataFrame([x for c in gens_ for (p, [x]) in c])

    def write(self, file_path=None, data_format=None):
        # #' @description export pedigree data in the old style cosegregation program.
        # #' @param file_name file name path.
        # oldstyle = function(file_name) {
        #     self$ped %>%
        # select(id,f,m,proband,age,gender,ageOnsetBC1,ageOnsetBC2,ageOnsetOC, genotype) %>%
        # write_tsv(file_name, col_names = FALSE)
        # },

        #
        # freestyle
        #
        return self
