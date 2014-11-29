# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 16:58:15 2014

@author: ubuntudido
"""



import SimPyNet
import simpy

def f(data):
    
    print ('B ha finito di elaborare %s')%(data)
    
def f2(data):
    
    print ('C ha finito di elaborare %s')%(data)
    
def start(Obj,data):
    
    print ('%f %s ha inviato il dato %s sul link %s')%(Obj.env.now, Obj.name,data.name,Obj.next_connection.name)
    
def R18():
    
    size_packet=8000 # in bits
    num_packets=1
    list_data=[]
    #err_prob=0
    #loss_prob=0.03

    rate_link= 2000000 # bits/s
    delay_prop_link=0.01 # m/s
    #delay_proc_router=0.01
    #queue_router=2

    for i in range(num_packets):
        list_data.append(SimPyNet.Databits(size_packet, i))
   
    env=simpy.Environment()
    
    A=SimPyNet.Node(env,'A')
    B=SimPyNet.Node(env,'B')
    C=SimPyNet.Node(env,'C')
    B.shape_handler(f)
    C.shape_handler(f2)

    l1=SimPyNet.Link(env,rate_link,delay_prop_link)

    l1.connect(A)
    l1.connect(B)
    l1.connect(C)
    #SimPyNet.physical.link_agent.disconnect(l1, C)
    A.send_data(list_data)
    
    env.run(until=1000)
    

def R19a():
    
    env=simpy.Environment()

    list_data=[]
    size_packet=10000 # bits
    num_packets=100000
    
    for i in xrange(num_packets):
        list_data.append(physical.Databits(i,size_packet))
    
    A=physical.Host(env,'A',list_data)
    B=physical.Host(env,'B',[])

    
    l3 =physical.Link(env,'l2',1000000)
    l2 =physical.Link(env,'l2',2000000)
    l1=physical.Link(env,'l1',500000)


    A.addHandler(l1.getHandler())
    l1.addHandler(l2.getHandler())
    l2.addHandler(l3.getHandler())
    l3.addHandler(B.getHandler())

    env.run(until=1000)
    print B.received_data/1000
    
def R19b():
    
    env=simpy.Environment()
    
    list_data=[]
    size_packet=1000 # bits
    num_packets=32000
    
    for i in xrange(num_packets):
        list_data.append(physical.Databits(i,size_packet))
    
    A=physical.Host(env,'A',list_data)
    B=physical.Host(env,'B',[])

    
    l3 =physical.Link(env,'l3',1000000)
    l2 =physical.Link(env,'l2',2000000)
    l1=physical.Link(env,'l1',500000)

    A.addHandler(l1.getHandler())
    l1.addHandler(l2.getHandler())
    l2.addHandler(l3.getHandler())
    l3.addHandler(B.getHandler())

    env.run(until=1000)

def R19c1():
    
    env=simpy.Environment()
   
    list_data=[]
    size_packet=10000 # bits
    num_packets=100000
    
    for i in xrange(num_packets):
        list_data.append(physical.Databits(i,size_packet))
    
    A=physical.Host(env,'A',list_data)
    B=physical.Host(env,'B',[])

    
    l3 =physical.Link(env,'l3',1000000)
    l2 =physical.Link(env,'l2',100000)
    l1=physical.Link(env,'l1',500000)

    A.addHandler(l1.getHandler())
    l1.addHandler(l2.getHandler())
    l2.addHandler(l3.getHandler())
    l3.addHandler(B.getHandler())

    env.run(until=1000)
    print B.received_data/1000 #B.time_last_packet
    
def R19c2():
    
    env=simpy.Environment()
    
    list_data=[]
    size_packet=1000 # bits
    num_packets=32000
    
    for i in xrange(num_packets):
        list_data.append(physical.Databits(i,size_packet))
    
    A=physical.Host(env,'A',list_data)
    B=physical.Host(env,'B',[])

    
    l3 =physical.Link(env,'l3',1000000)
    l2 =physical.Link(env,'l2',100000)
    l1=physical.Link(env,'l1',500000)

    A.addHandler(l1.getHandler())
    l1.addHandler(l2.getHandler())
    l2.addHandler(l3.getHandler())
    l3.addHandler(B.getHandler())

    env.run(until=1000)
    print B.received_data/B.time_last_packet

def P10():
    
    env=simpy.Environment()
    
    list_data=[]
    size_packet=12000 # bits
    num_packets=1
    
    for i in xrange(num_packets):
        list_data.append(physical.Databits(i,size_packet))
    
    A=physical.Host(env,'A',list_data)
    B=physical.Host(env,'B',[])
    
    l3 =physical.Link(env,'l3',2000000,0.004,deterministic=True)
    l2 =physical.Link(env,'l2',2000000,0.016,deterministic=True)
    l1=physical.Link(env,'l1',2000000,0.02,deterministic=True) #ms

    n1=physical.Node(env,'n1',0.003)# ms
    n2=physical.Node(env,'n2',0.003)# ms
    
      
    A.addHandler(l1.getHandler())  
    l1.addHandler(n1.getHandler())
    n1.addHandler(l2.getHandler())
    l2.addHandler(n2.getHandler())
    n2.addHandler(l3.getHandler())
    l3.addHandler(B.getHandler())
    
    env.run(until=1000)
    
    
    

    
    
    
R18()
#R19a()
#R19b()
#R19c1()
#R19c2()
#P10()