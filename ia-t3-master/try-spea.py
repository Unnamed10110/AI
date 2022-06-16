#!/usr/bin/env python
# -*- coding: utf-8 -*-
from solution import *
from metric import *
import timeit
import spea
import moacs
import sys,os


def main():
    # Recibe por terminal el nro. de instancia a resolver.
    #print(sys.argv)
    #os.system('pause')
    instance = int(sys.argv[1]) - 1
    #print(instance),os.system('pause')
    pareto_set_true = ParetoSet(None)

    ##################################
    pareto_set_spea = spea.test_qap(i=instance)
    pareto_front_spea = ParetoFront(pareto_set_spea)
    pareto_set_true.update(pareto_set_spea.solutions)
    pareto_front_true = ParetoFront(pareto_set_true)

    for i in range(2):
        aa = pareto_front_true
        pareto_set_spea = spea.test_qap(i=instance)
        pareto_front_spea = ParetoFront(pareto_set_spea)
        pareto_set_true.update(pareto_set_spea.solutions)
        pareto_front_true = ParetoFront(pareto_set_true)
        m1 = DistanceMetric(pareto_front_true)
        m11= DistanceMetric(aa)
        #print(i,'-----------')
        if (m1.evaluate(pareto_front_spea)< m11.evaluate(pareto_front_spea)):
            pareto_front_true=aa


    ##################################
    for i in range(5):
        print('--------------\nejecución: ',i+1)
        start = timeit.default_timer()
        pareto_set_spea = spea.test_qap(i = instance)
        pareto_front_spea = ParetoFront(pareto_set_spea)
        #pareto_set_true.update(pareto_set_spea.solutions)
        #print(pareto_set_spea.solutions[1].solution)
        #print(len(pareto_set_spea.solutions)), os.system('pause')
        #print('fin spea')
        #os.system('pause')
        elapsed = timeit.default_timer() - start
        print("---  %s segundos     ---" % elapsed)
        print("---  %2.20f horas    ---" % (float(elapsed) / 3600))

        #pareto_front_true = ParetoFront(pareto_set_true)
        #pareto_front_true.draw()

        m1 = DistanceMetric(pareto_front_true)
        m2 = DistributionMetric(1000.0)
        m3 = ExtensionMetric()
        m4 = ErrorMetric(pareto_front_true)

        print("\nSPEA:")
        print("Distancia: " + str(m1.evaluate(pareto_front_spea)))
        print("Distribución:" + str(m2.evaluate(pareto_front_spea)))
        print("Extensión:" +  str(m3.evaluate(pareto_front_spea)))
        print("Error:" + str(m4.evaluate(pareto_front_spea)))

    return 0

if __name__ == '__main__':
    main()

