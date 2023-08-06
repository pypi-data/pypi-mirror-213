import csv
import os.path

import pandas as pd
import numpy as np
import scipy.stats as stats
from pedanlib import Pedigree
import math

import warnings

class Risk:
    rsk = None
    pop = None

    def __init__(self):
        self.rsk = self.rskfile(self.risk_file())
        self.pop = None

    @staticmethod
    def risk_file():
        return os.path.join(os.path.dirname(__file__), 'data/risk1_lognormal_pr_v03.csv')

    @staticmethod
    def rskfile(file_path):
        """

        :param file_path:
        :return:
        """
        with open(file_path, 'rb') as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.readline().decode('utf-8'))
            df = pd.read_csv(file_path, sep=dialect.delimiter)
        return df

    def crisk(self, ctype, gender, variant, dist):
        df = self.rsk

        """
        log-normal paramters only available for female, breast cancer for variants {BRCA1, BRCA2} 
        """

        df = df.loc[(df['p'] == self.pop) &
                    (df['ctype'] == ctype) &
                    (df['sex'] == gender) &
                    (df['carrier'] == variant) &
                    (df['dist'] == dist)]
        if df.empty:
            return None
        else:
            s = pd.Series({'mu': df['mu'].to_numpy()[0], 'sigma': df['sigma'].to_numpy()[0],
                           'r': df['r'].to_numpy()[0]})
            if pd.isna(s.mu):
                return None
            else:
                return s

    def set_population(self, pop):
        self.pop = pop


class Ped:
    members = None
    rng = None

    def __init__(self, ped):
        self.members = {row.id: row for (_, row) in ped.iterrows()}
        self.rng = range(1, self.size() + 1)

    def get(self, i):
        return self.members[i]

    def age_onsets(self, i):
        m = self.get(i)
        return m[[v for v in m.keys() if "ageOnset" in v]]

    def is_male(self, i):
        return self.get(i)['gender'] == 1

    def is_female(self, i):
        return self.get(i)['gender'] == 2

    def size(self):
        return len(self.members)

    def range(self):
        return self.rng

    def gender(self, i):
        if self.is_female(i):
            return 'female'
        else:
            return 'male'


class Coseg:
    pedigree = None
    pedigree_targets = None
    ped = None
    rsk = None
    pop = None
    pen = None
    gs_ = None
    ps_ = None
    cfg = None

    assoc = {1: ['bc', 'pa', 'pr'], 2: ['bc', 'pa', 'ov']}
    variants = ['brca1', 'brca2', 'palb2']
    carrier = ['non.carrier', 'brca1', 'brca2', 'palb2']
    log = None
    poetry = 'Risk file v3'

    def __init__(self, pedigree, population, enum=True):
        """
        Need to call self.enum_geno() outside init !!!
        Args:
            pedigree:
            population:
        """
        self.pedigree_targets = {v:Pedigree(pedigree=pedigree, tv=v) for v in self.variants}
        self.pedigree = self.pedigree_targets['brca1']
        self.ped = Ped(self.pedigree.ped)
        self.rsk = Risk()
        self.set_population(population)
        if enum:
            self.init_enum()
        # else:
        #     warnings.warn('run enumeration manually !')

    def init_enum(self, dist='normal'):
        self.pedigree.enum_geno_par_pg()
        self.gs_ = self.pedigree.gs
        self.ps_ = pd.Series(self.pedigree.ps)
        self.cfg = self.pedigree.configurations()
        self.set_pen(dist)

    def v2i(self, variant):
        return self.carrier.index(variant)

    def i2v(self, i):
        return self.carrier[i]

    def set_penetrance(self, pop, dist):
        self.set_population(pop)
        self.set_pen(dist)

    def gs(self):
        return self.gs_

    def ps(self):
        return self.ps_

    def configurations(self):
        return self.cfg

    def set_population(self, pop):
        """
        Deprecated

        Args:
            pop:

        Returns:

        """
        self.rsk.set_population(pop)
        self.pop = pop

    def get_pop(self):
        """
        The population is set in class init.
        Returns: either {None, NL, UK}
        """
        return self.pop

    def gn(self, i, variant, dist):
        """

        :param i:
        :param variant:
        :param dist:
        :return:
        """
        age_onsets = self.ped.age_onsets(i)
        gender_ = self.ped.get(i).gender
        params = pd.Series(
            {ctype: self.rsk.crisk(ctype, gender_, variant, dist) for ctype in self.assoc[gender_]})

        return age_onsets, params

    @staticmethod
    def pdf(age, ctype):
        """
        dnormal

        :param age:
        :param ctype:
        :return:
        """
        if ctype is not None:
            return stats.norm.pdf(age, ctype.mu, ctype.sigma) * ctype.r
        else:
            return 1

    @staticmethod
    def lpdf(age, ctype):
        """
        dnormal (log)

        :param age:
        :param ctype:
        :return:
        """
        if ctype is not None:
            lognorm_ = stats.lognorm(s=ctype.sigma, scale=math.exp(ctype.mu))
            return lognorm_.pdf(age) * ctype.r
        else:
            return 1


    @staticmethod
    def cdf(age, ctype):
        """
        pnormal

        :param age:
        :param ctype:
        :return:
        """
        if ctype is not None:
            return stats.norm.cdf(age, ctype.mu, ctype.sigma) * ctype.r
        else:
            return 0

    @staticmethod
    def lcdf(age, ctype):
        """
        pnormal (log)

        :param age:
        :param ctype:
        :return:
        """
        if ctype is not None:
            lognorm_ = stats.lognorm(s=ctype.sigma, scale=math.exp(ctype.mu))
            return lognorm_.cdf(age) * ctype.r
        else:
            return 0

    def logger(self, x):
        if self.log is None:
            self.log = pd.DataFrame(columns=x.keys())
            self.log.loc[len(self.log)] = x
        else:
            self.log.loc[len(self.log)] = x

    def dist_matcher(self, dist):
        match dist:
            case 'normal':
                return self.pdf, self.cdf
            case 'lognormal':
                return self.lpdf, self.lcdf

    def bc(self, i, variant, dist='normal'):
        ao, params = self.gn(i, variant, dist)
        age_ = self.ped.get(i).age
        pdf, cdf = self.dist_matcher(dist)
        if self.ped.is_female(i):
            if ao.ageOnsetBC1 == 0:
                return 1 - cdf(age_, params.bc)
            elif (ao.ageOnsetBC1 > 0) & (ao.ageOnsetBC2 == 0):
                return pdf(ao.ageOnsetBC1, params.bc)
            elif (ao.ageOnsetBC1 > 0) & (ao.ageOnsetBC2 > 0):
                bc1_cdf = np.sqrt(1 - cdf(ao.ageOnsetBC1, params.bc))
                bc2_cdf = np.sqrt(1 - cdf(ao.ageOnsetBC2, params.bc))
                bc1_pdf = pdf(ao.ageOnsetBC1, params.bc)
                bc2_pdf = pdf(ao.ageOnsetBC2, params.bc)
                # if i == 12:
                #     print(f" {bc1_cdf}\t{bc2_cdf}\t{bc1_pdf}\t{bc2_pdf}")
                return 0.25 * bc1_pdf * bc2_pdf / (bc1_cdf * bc2_cdf)
        else:
            if ao.ageOnsetBC1 > 0:
                return pdf(ao.ageOnsetBC1, params.bc)
            else:
                return 1 - cdf(age_, params.bc)

    def pa(self, i, variant, dist='normal'):
        ao, params = self.gn(i, variant, dist)
        age_ = self.ped.get(i).age
        pdf, cdf = self.dist_matcher(dist)
        if ao.ageOnsetPA > 0:
            return pdf(ao.ageOnsetPA, params.pa)
        else:
            return 1 - cdf(age_, params.pa)

    def pr(self, i, variant, dist='normal'):
        ao, params = self.gn(i, variant, dist)
        age_ = self.ped.get(i).age
        pdf, cdf = self.dist_matcher(dist)

        if ao.ageOnsetPR > 0:
            return pdf(ao.ageOnsetPR, params.pr)
        else:
            return 1 - cdf(age_, params.pr)

    def ov(self, i, variant, dist='normal'):
        ao, params = self.gn(i, variant, dist)
        age_ = self.ped.get(i).age

        pdf, cdf = self.dist_matcher(dist)
        if ao.ageOnsetOC > 0:
            return pdf(ao.ageOnsetOC, params.ov)
        else:
            return 1 - cdf(age_, params.ov)

    def penetrance(self, i, variant, dist):
        """


        Returns: (i, variant, non_carrier, carrier)
        :param i: pedigree member i
        :param dist: controls the distribution {normal, log-normal}  on female breast cancer.
        :param variant: 1..3
        """
        ao, params = self.gn(i, variant, dist)

        nc_idx = self.v2i('non.carrier')
        if self.ped.is_female(i):
            """ female 
            """
            non_carrier = self.bc(i, nc_idx) * self.ov(i, nc_idx) * self.pa(i, nc_idx)
            """ option: in BRCA1/BRCA2 (1/2) to take dist={normal,lognormal}
            """
            if variant in [1, 2]:
                carrier = self.bc(i, variant, dist=dist)
            else:
                carrier = self.bc(i, variant)  # dist=normal
            carrier = carrier * self.ov(i, variant) * self.pa(i, variant)
        else:
            """ male
            """
            non_carrier = self.bc(i, nc_idx) * self.pa(i, nc_idx)
            carrier = self.bc(i, variant) * self.pa(i, variant)

            if variant not in [1, 3]:
                non_carrier = non_carrier * self.pr(i, nc_idx)
                carrier = carrier * self.pr(i, variant)
        return i, variant, non_carrier, carrier

    def set_pen(self, dist):
        df = [self.penetrance(i, v, dist) for i in self.ped.range() for v in range(1, len(self.carrier))]
        self.pen = pd.DataFrame(df, columns=['id', 'variant', 'non.carrier', 'carrier'])

    def get_pen(self, variant):
        df = self.pen[self.pen.variant == variant].sort_values('id')[['non.carrier', 'carrier']]. \
            rename(columns={'non.carrier': 'non.carrier', 'carrier': self.carrier[variant]})
        df.reset_index(drop=True, inplace=True)
        df.index += 1
        return df

    def likin(self, variant):
        """

        Args:
            variant: {brca1, brca2, palb2}

        Returns:
        """
        P = self.get_pen(self.v2i(variant))
        G = self.gs()
        C = pd.concat([P[[variant]].transpose()] * G.shape[0]). \
            reset_index().drop('index', axis=1)
        N = pd.concat([P[['non.carrier']].transpose()] * G.shape[0]). \
            reset_index().drop('index', axis=1)
        return ((1 - G.multiply(1.0)).multiply(N) + G.multiply(C)).product(axis=1)

    def observed(self):
        target = self.pedigree.observed(value=True)
        obs = self.pedigree.observed()
        return self.gs().apply(lambda x: all(np.array(x[obs]) == np.array(target)), axis=1)  # np.array due to warning by PyCharm

    def lr(self, variant):
        """

        :param variant: {brca1, brca2, palb2}
        :return:
        """

        self.pedigree = self.pedigree_targets[variant]

        tbl = pd.DataFrame({'obs': self.observed(), 'p': self.ps(), 'prod_pen': self.likin(variant)})
        numer = tbl.groupby('obs').apply(lambda x: sum(x.p * x.prod_pen))[True]
        denom = tbl.apply(lambda x: x.p * x.prod_pen, axis=1).sum()
        # numer < - tbl % > % group_by(obs) % > % summarise(numer=sum((p * prod_pen))) % > % dplyr::filter(
        #     obs) % > % pull(numer)
        # denom < - tbl % > % summarise(denom=sum((p * prod_pen))) % > % pull(denom)
        # p_n < - tbl % > % filter(obs) % > % summarise(lrn=sum(p)) % > % pull(lrn)

        p_d = numer / denom
        p_n = tbl[tbl.obs].p.sum()
        return p_d / p_n

    def lrs(self):
        return pd.Series({v: self.lr(v) for v in self.variants})
