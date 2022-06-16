#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import *
from solution import *
import os

class Ant:
    def __init__(self, beta, ant_number, total_ants, ferom_mat, visib_mats, objectives):
        """
        @param ferom_mat: matriz de feromonas.
        @param visib_mats: matrices de visibilidad. Una por objetivo.
        @param objectives:
        """
        self.beta = beta
        self.ant_number = ant_number
        self.total_ants = total_ants
        self.ferom_mat = ferom_mat
        self.objectives = objectives
        self.visib_mats = visib_mats

    def build_solution(self):
        """
        Construye una solución al problema planteado.
        """
        raise NotImplementedError("build_solution method has to be implemented.")

    def probability(self, city_number, feasible_nodes):
        """
        @param city_number: ciudad actual.

        @feasible_nodes: lista de posibles ciudades a ser visitadas en el siguiente movimiento.
        """
        lamda = self.ant_number / self.total_ants  # lambda es una palabra reservada
        total = 0
        prob_list = list()  # cada elemento tiene el numero de ciudad y su probabilidad asociada
        for j in feasible_nodes:
            try:
                total += self.ferom_mat[city_number][j] * self.visib_mats[0][city_number][j] ** (lamda * self.beta) * \
                             self.visib_mats[1][city_number][j] ** ((1 - lamda) * self.beta)
            except:
                cc=0

        for j in feasible_nodes:
            try:
                prob = (self.ferom_mat[city_number][j] * self.visib_mats[0][city_number][j] ** (lamda * self.beta) \
                    * self.visib_mats[1][city_number][j] ** ((1 - lamda) * self.beta)) / total
                prob_list.append([j, prob])
            except:
                cc=0
        return prob_list


class MOACSAnt(Ant):
    def __init__(self, beta, ant_number, total_ants, ferom_mat, visib_mats, objectives, tausubzero, qsubzero, rho):
        Ant.__init__(self, beta, ant_number, total_ants, ferom_mat, visib_mats, objectives)
        self.tausubzero = tausubzero
        self.qsubzero = qsubzero
        self.rho = rho
        self.sum_obj = []
        for i in range(len(self.objectives)):
            self.sum_obj.insert(i, 0)  # inicializar suma de cada objetivo a 0

    def choose_next_node(self, city_number, feasible_nodes):
        lamda = self.ant_number / self.total_ants
        q = random()
        next_node=0
        if q < self.qsubzero:
            max_prob = 0
            max_node = 0
            tama=len(self.ferom_mat)
            #print(tama),os.system('pause')
            #print('posicion:',self.ferom_mat[city_number][tama-1],'(city_number,feasible_nodes):',feasible_nodes)
            #os.system('pause')
            #print('tamaño',tama)
            #for k in feasible_nodes:
                #print('par:',city_number,'-',k)
                #print(self.ferom_mat[city_number][k])
            #os.system('pause')
            for j in feasible_nodes:

                    #print('----------------------')
                    #print('tama-1:',tama-1)
                    #print('j=',j)
                    #print('number_city:',city_number)
                    #print('ferom_mat:',self.ferom_mat[city_number][j])
                    #print('visib_mats:',self.visib_mats[0][city_number][j])
                    try:
                        aux = self.ferom_mat[city_number][j] * self.visib_mats[0][city_number][j] ** (lamda * self.beta) * \
                                  self.visib_mats[1][city_number][j] ** ((1 - lamda) * self.beta)
                        if (aux > max_prob):
                            max_prob = aux
                            max_node = j
                    except:
                        cc=0



            next_node = max_node
        else:
            probs = self.probability(city_number, feasible_nodes)
            aux = [p[1] for p in probs]
            limits = [sum(aux[:i + 1]) for i in range(len(aux))]
            aux = random()
            for i in range(len(limits)):
                if aux <= limits[i]:
                    next_node = probs[i][0]
                    break
        return next_node

    def build_solution(self):
        sol_len = len(self.ferom_mat)
        sol = [randint(0, sol_len - 1)]
        self.average_obj = []

        for i in range(len(self.objectives)):
            self.sum_obj[i] = 0  # inicializar suma de cada objetivo a 0

        while (len(sol) < sol_len):
            actual_node = sol[-1]
            next_node = self.choose_next_node(actual_node, [i for i in range(sol_len) if i not in sol])
            for j in range(len(self.objectives)):
                self.sum_obj[j] = self.sum_obj[j] + self.objectives[j].cost_i_to_j(actual_node,
                                                                                   next_node)  # actualizar la suma de objetivos
                # self.sum_obj[j] = self.sum_obj[j] + self.objectives[j].mat[actual_node][next_node] #actualizar la suma de objetivos
            # #actualizacion de feromonas
            self.ferom_mat[actual_node][next_node] = (1 - self.rho) * self.ferom_mat[actual_node][
                next_node] + self.rho * self.tausubzero
            sol.append(next_node)

        for i in range(len(self.objectives)):
            self.average_obj.insert(i, self.sum_obj[i] / sol_len)

        return Solution(sol, self.objectives)


