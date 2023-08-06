import pandas as pd
import re
import os
import json

class CanRisk:
    """
    CanRisk class


    Methods:
        read
        write
        carrier : {0,1,2} => {0:N, 0:P, 0:0} = {non-carrier, carrier, unknown}
    """
    df: pd.DataFrame = None
    cr_file = None
    version = None
    cr_meta = None
    header = {}
    __age_onsets = ['BC1', 'BC2', 'OC', 'PRO', 'PAN']
    __genes = ['BRCA1', 'BRCA2', 'PALB2']
    summary_ = None

    @staticmethod
    def canrisk_meta():
        cr_meta_file = os.path.join(os.path.dirname(__file__), 'data/canrisk.json')
        with open(cr_meta_file) as crm:
            meta_ = json.load(crm)
        return {v['name'].lower(): v for v in meta_}

    def __init__(self, file_path=None):
        """

        :param file_path:
        """
        self.cr_meta = self.canrisk_meta()

        if file_path is not None:
            self.cr_file = file_path
            with open(self.cr_file, "r") as file:
                line = file.readline()
                m = re.search('(?<=##)CanRisk', line)
                if m is not None:
                    self.read()

    def get_meta(self, tag='description'):
        ped_params = {k.lower(): self.header[k] for k in self.header.keys()}
        meta_ = {}
        for param in self.cr_meta.keys():
            if param in ped_params.keys():
                meta_[self.cr_meta[param][tag]] = ped_params[param]
            else:
                meta_[self.cr_meta[param][tag]] = None

        return meta_

    def read(self):
        res = []  # keep track of meta info
        df = None  # observations
        i = 0  # index

        with open(self.cr_file, "r") as file:
            for line in file:
                m = re.search('(?<=##)\w*', line)
                if m is None:
                    res.append('obs')
                    df.loc[i] = line.split()
                    i = i + 1
                else:
                    field = m.group(0)
                    if field == 'FamID':
                        df = pd.DataFrame(columns=tuple(line.replace('##', '').split()))
                    elif field =='CanRisk':
                        self.version = line.split()[1]
                    else:
                        prefix_ = line.rstrip().split('=')[0] + '='
                        self.header[field] = line.rstrip().replace(prefix_, '')

                        # fld = re.search('(?<=##' + field + ')=\w*', line)
                        # if fld is not None:
                        #     self.header[field] = fld.group(0).replace('=', '')
                        # else:
                        #     self.header[field] = line.rstrip().split(' ')[1]

            for v in ['Target', 'Age', 'Yob', 'BC1', 'BC2', 'OC', 'PRO', 'PAN']:
                df[v] = df[v].astype(int)
            # Updating Name to IndivID
            # df['Name'] = pd.Series([df['IndivID'][i] if df['Name'][i] == 'NA' else df['Name'][i] for i in df['Name'].index])
            self.df = df
        return None

    @staticmethod
    def carrier(x):
        return {0: "0:N", 1: "0:P", 2: "0:0"}[x]

    def write_old_format(self, df: pd.DataFrame, cr_version="1.0", file=None, target=None):
        """


        :param df: cosegregation program data format
        :param cr_version: CanRisk version, default=1.0
        :param file: .txt file to write to.
        :param target: set of (key,value) pairs to add to meta data part.
        :return:
        """

        if target is None:
            target = {}
        local_header = ["id", "f", "m", "name", "age", "ageOnsetBC1", "ageOnsetBC2", "ageOnsetOC", "ageOnsetPR",
                        "ageOnsetPA", "gender", "genotype", "proband"]

        # df may have more columns than the defined 'local_header'
        if set(local_header).issubset(set(df.columns)):
            raise Exception("invalid local format")

        # Header
        """
        ##CanRisk 1.0
        """
        header = ["FamID", "Name", "Target", "IndivID", "FathID", "MothID", "Sex",
                  "MZtwin", "Dead", "Age", "Yob", "BC1", "BC2", "OC", "PRO", "PAN",
                  "Ashkn", "BRCA1", "BRCA2", "PALB2", "ATM", "CHEK2", "RAD51D",
                  "RAD51C", "BRIP1", "ER:PR:HER2:CK14:CK56"]

        res = ["##CanRisk " + str(cr_version)]

        if len(target) != 0:
            for k, v in target.items():
                res = res + ["##" + "=".join(list(map(lambda x: str(x), [k, v])))]

        res = res + ["##" + "\t".join(list(map(lambda x: str(x), header)))]

        # Data
        # FamID  : xxxx
        # Name   : NA
        # Target : proband
        # IndivID: id
        # FathID : f
        # MothID : m
        # Sex    : gender
        # MZtwin : 0
        # Dead   : 0   <= 0=alive 1=dead, unknown not possible !!!
        # Age    : age (last follow)
        # Yob    : 0
        #
        # CanRisk specification on age onsets BC1, BC2, OC, PRO, PAN etc. :
        #      0       = unaffected,
        #      integer = age at diagnosis,
        #      AU      = unknown age at diagnosis (affected unknown)
        #
        # BC1    : ageOnsetBC1
        # BC2    : ageOnsetBC2
        # OC     : ageOnsetOC
        # PRO    : ageOnsetPR = 0
        # PAN    : ageOnsetPA = 0
        # Ashkn  : 0
        #
        #
        # BRCA1 BRCA2 PALB2 ATM CHEK2 RAD51D RAD51C BRIP1 ('genetic test type':'result'):
        #             genetic test type :  0=untested, S=mutation search,T=direct gene test
        #             result : 0=untested, P=positive,N=negative
        # Note: currently only  BRCA1, BRCA2 and PALB2 are represented in the 'genotype' field
        # of the co-segregation data format with values 1,2 and 3 respectively.
        #
        # BRCA1  : genotype  => 0:{0,P,N}
        # BRCA2  : genotype  => 0:{0,P,N}
        # PALB2  : genotype  => 0:{0,P,N}
        # ATM    : 0:0
        # CHEK2  : 0:0
        # RAD51D : 0:0
        # RAD51C : 0:0
        # BRIP1  : 0:0
        # ER:PR:HER2:CK14:CK56 : 0:0:0:0:0
        df_ = pd.DataFrame({'FamID': 'xxx0',
                            'Name': 'NA',
                            'Target': map(int, df.proband.to_list()),
                            'IndivID': map(int, df.id.to_list()),
                            'FathID': map(int, df.f.to_list()),
                            'MothID': map(int, df.m.to_list()),
                            'Sex': ["M" if v == 1 else "F" for v in map(int, df.gender.to_list())],
                            'MZtwin': 0,
                            'Dead': 0,  # 0=alive 1=dead, unknown not possible !!!
                            'Age': map(int, df.age.to_list()),  # (last follow)
                            'Yob': 0,
                            'BC1': map(int, df.ageOnsetBC1.to_list()),
                            'BC2': map(int, df.ageOnsetBC2.to_list()),
                            'OC': map(int, df.ageOnsetOC.to_list()),
                            'PRO': map(int, df.ageOnsetPR.to_list()),
                            'PAN': map(int, df.ageOnsetPA.to_list()),
                            'Ashkn': 0,
                            'BRCA1': map(self.carrier, df.genotype.to_list()),
                            'BRCA2': map(self.carrier, df.genotype.to_list()),
                            'PALB2': map(self.carrier, df.genotype.to_list()),
                            'ATM': "0:0",
                            'CHEK2': "0:0",
                            'RAD51D': "0:0",
                            'RAD51C': "0:0",
                            'BRIP1': "0:0",
                            'ER:PR:HER2:CK14:CK56': "0:0:0:0:0"
                            })
        for rec in df_.to_records(index=False):
            res = res + ['\t'.join(map(str, rec))]
        res = "\n".join(res)
        if file is not None:
            f = open(file, "w")
            f.write(res)
            f.close()
        else:
            return res

    def to_basic_format(self, tv='brca1'):

        def genotype(brca1, brca2, palb2, tv):

            def matcher(x):
                match x:
                    case 'P':
                        return 1
                    case 'N':
                        return 0
                    case _:
                        return 2

            variants = {'brca1': brca1, 'brca2': brca2, 'palb2': palb2}
            return pd.Series([matcher(v) for v in pd.Series([re.sub('^.:', '', g) for g in variants[tv]])])

        def age_onset(ao):
            def matcher(x):
                if str(x) in ['0', 'AU']:
                    return 0
                else:
                    return int(x)
            return pd.Series([matcher(v) for v in ao])

        def name2index():
            map_ = {n: i+1 for i, n in enumerate(self.df.IndivID)}
            map_['0'] = 0
            father = pd.Series([map_[v] for v in self.df.FathID])
            mother = pd.Series([map_[v] for v in self.df.MothID])
            del map_['0']
            return pd.Series(map_.values()), father, mother

        id_, f_, m_ = name2index()
        d = {'id': id_,
             'f': f_,
             'm': m_,
             'proband': self.df.Target,
             'age': self.df.Age,
             'gender': pd.get_dummies(self.df.Sex).F + 1,
             'ageOnsetBC1': age_onset(self.df.BC1),
             'ageOnsetBC2': age_onset(self.df.BC2),
             'ageOnsetOC': age_onset(self.df.OC),
             'ageOnsetPA': age_onset(self.df.PAN),
             'ageOnsetPR': age_onset(self.df.PRO),
             'genotype': genotype(self.df.BRCA1, self.df.BRCA2, self.df.PALB2, tv=tv),
             'name': self.df.IndivID}

        return pd.DataFrame(d)

        # mutate(id=IndivID,
        #        f=FathID,
        #        m=MothID,
        #        proband= as.numeric(Target),
        #                    age=as.numeric(Age),
        #                           gender=ifelse(Sex=="M",1,2),
        #                                  ageOnsetBC1=ifelse(BC1 %in% c("0","AU"),0,as.numeric(BC1)) ,
        # ageOnsetBC2=ifelse(BC2 %in% c("0","AU"),0,as.numeric(BC2)) ,
        # ageOnsetOC=ifelse(OC %in% c("0","AU"),0,as.numeric(OC)),
        # ageOnsetPA=ifelse(PAN %in% c("0","AU"),0,as.numeric(PAN)),
        # ageOnsetPR=ifelse(PRO %in% c("0","AU"),0,as.numeric(PRO)),
        # # "genotype" : Genotype (0 non-carrier, 1 carrier and 2 for unknown genotypes)
        # genotype=brc12_test(BRCA1,BRCA2,PALB2),
        #          name=IndivID
        # ) %>%

    def proband(self, gene=None, genotype=None):
        if gene is None:
            raise Exception("Missing gene argument, use gene={'BRCA1'| 'BRCA2' | 'PALB2'}")
        if genotype is None:
            return self.df[self.df.Target == 1][gene]
        else:
            self.df.loc[self.df.Target == 1, gene] = genotype

    def genotypes(self):
        return {gene: self.proband(gene=gene).to_list()[0] for gene in ['BRCA1', 'BRCA2', 'PALB2']}

    def to_tsv(self, file_path):
        self.df.to_csv(path_or_buf=file_path, sep='\t', index=False)

    def gene_summary(self):
        d = {gene: self.df[self.df[gene] != '0:0'][gene].to_list() for gene in ['BRCA1', 'BRCA2', 'PALB2']}
        genotype_ = pd.DataFrame(d.items(), columns=['gene', 'genotype'])
        d2 = {gene: self.df[self.df[gene] != '0:0']['Target'].to_list() for gene in ['BRCA1', 'BRCA2', 'PALB2']}
        proband_ = pd.DataFrame(d2.items(), columns=['gene', 'proband'])
        df = pd.merge(genotype_, proband_, on=['gene'])
        df = df.loc[list(map(lambda xx: len(xx) > 0, df.genotype))]
        # if len(df) > 1:
        #    raise Exception("Multiple genes genotyped !")
        return df

    def genes(self):
        return self.df[self.__genes]

    def age_onsets(self):
        df_ = self.df[self.__age_onsets]
        return pd.Series([sum(df_[s] != 0) for s in df_], index=[df_.columns])
