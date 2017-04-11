from flask import Flask, request, render_template, url_for, flash, redirect, session,make_response,jsonify
from functools import wraps,update_wrapper
from wsgiref.handlers import format_date_time

import random
import math
import copy

import subprocess
import time
from subprocess import *

def check_intersection(edge,p3,p4):
		#do something here
		pt1=(edge.p1.x,edge.p1.y)
		pt2=(edge.p2.x,edge.p2.y)
		pt3=(p3.x,p3.y)
		pt4=(p4.x,p4.y)
		#print "yo"
		result=intersectLines(pt1,pt2,pt3,pt4)
		# print result
		if(result[2]==0):
			return False
		x=result[0]
		y=result[1]
		#print x,y,p3.id,p4.id
		if(x>=min(p3.x,p4.x) and y>=min(p3.y,p4.y) and x<=max(p3.x,p4.x) and y<=max(p3.y,p4.y)):
			if (x,y)==pt1 or (x,y)==pt2 or (x,y)==pt3 or (x,y)==pt4:
				return False
			else: return True
		return False


def intersectLines(pt1, pt2, ptA, ptB ): 
    """ this returns the intersection of Line(pt1,pt2) and Line(ptA,ptB)
        
        returns a tuple: (xi, yi, valid, r, s), where
        (xi, yi) is the intersection
        r is the scalar multiple such that (xi,yi) = pt1 + r*(pt2-pt1)
        s is the scalar multiple such that (xi,yi) = pt1 + s*(ptB-ptA)
            valid == 0 if there are 0 or inf. intersections (invalid)
            valid == 1 if it has a unique intersection ON the segment    """

    DET_TOLERANCE = 0.00000001

    x1, y1 = pt1;   x2, y2 = pt2
    dx1 = x2 - x1;  dy1 = y2 - y1
    x, y = ptA;   xB, yB = ptB;
    dx = xB - x;  dy = yB - y;

    # we need to find the (typically unique) values of r and s
    # that will satisfy
    #
    # (x1, y1) + r(dx1, dy1) = (x, y) + s(dx, dy)
    #
    # which is the same as
    #
    #    [ dx1  -dx ][ r ] = [ x-x1 ]
    #    [ dy1  -dy ][ s ] = [ y-y1 ]
    #
    # whose solution is
    #
    #    [ r ] = _1_  [  -dy   dx ] [ x-x1 ]
    #    [ s ] = DET  [ -dy1  dx1 ] [ y-y1 ]
    #
    # where DET = (-dx1 * dy + dy1 * dx)
    #
    # if DET is too small, they're parallel
    #
    DET = (-dx1 * dy + dy1 * dx)

    if math.fabs(DET) < DET_TOLERANCE: return (0,0,0,0,0)

    # now, the determinant should be OK
    DETinv = 1.0/DET

    # find the scalar amount along the "self" segment
    r = DETinv * (-dy  * (x-x1) +  dx * (y-y1))

    # find the scalar amount along the input line
    s = DETinv * (-dy1 * (x-x1) + dx1 * (y-y1))

    # return the average of the two descriptions
    xi = (x1 + r*dx1 + x + s*dx)/2.0
    yi = (y1 + r*dy1 + y + s*dy)/2.0
    return ( xi, yi, 1, r, s )


def lie_on_line(point,p1,p2):
	if ((p2.y-p1.y)*(point.x-p1.x))==((point.y-p1.y)*(p2.x-p1.x)):
		if(point.x>=min(p1.x,p2.x) and point.y >= min(p1.y,p2.y) and point.x<=max(p1.x,p2.x) and point.y <= max(p1.y,p2.y)):
			#print p1.x,p1.y,p2.x,p2.y,point.x,point.y
			return True
	return False



class graph:
	def __init__(self, max_x, max_y, prob, number):
	 	self.max_x = max_x
	 	self.max_y = max_y
	 	self.prob = prob
	 	self.number = number
	 	self.points = []
	 	self.edges = []

	class point:
		def __init__(self,x,y,id):
			self.x = x
			self.y = y
			self.id = id
	class edge:
		def __init__(self,p1,p2):
			self.p1 = p1
			self.p2 = p2

	def add_points(self):
		for i in range(0,self.number):
			p = self.point(random.randint(0, self.max_x),random.randint(0, self.max_y),i)
			if p in self.points:
				i=i-1
				continue
			self.points.append(p)
		#print self.points[0]
	
	def print_points(self):
		for i in range(0,self.number):
			print self.points[i].x,self.points[i].y
		print "Edges"
		for i in range(0,len(self.edges)):
			print self.edges[i].p1.id,self.edges[i].p2.id
	
	def check(self,i,j):
		p1=self.points[i]
		p2=self.points[j]
		for edge in self.edges:
			if check_intersection(edge,p1,p2):
				return False
		# for point in self.points:
		# 	if point==p1 or point == p2:
		# 		continue
		# 	if lie_on_line(point,p1,p2):
		# 		return False
		return True




	def add_edges(self):
		# self.edges.append(self.edge(self.points[0],self.points[1]))
		# print self.edges[0]
		for i in range(0,self.number):
			for j in range(i+1,self.number):
				if random.random()>self.prob: continue
				if self.check(i,j):
					self.edges.append(self.edge(self.points[i],self.points[j]))
		#print len(self.edges)

	def adj_matrix(self):
		p=self.number
		Matrix = [[0 for x in range(p)] for y in range(p)]
		for e in self.edges:
			Matrix[e.p1.id][e.p2.id]=1
			Matrix[e.p2.id][e.p1.id]=1
		return Matrix


class node:
	def __init__(self,id,colours):
		self.id=id
		self.domain=[]
		self.color=None
		for i in range(colours):
			self.domain.append(i)

class colouring:
	def __init__(self,colours,adj_matrix):
		self.colours=colours
		self.adj_matrix=adj_matrix
		self.answer=None
		# self.nodes=[]
		# for i in range(len(adj_matrix)):
		# 	self.nodes.append(node(i,colours))

	def check_assignment(assignment):
		#to check if all nodes are allocated a color
		for i in assignment:
			if i==-1:
				return False
		return True

	def select_unassigned_var(type,nodes):
		if type==0:
			for node in nodes:
				if node.color==None:
					return node

		if type==1:
			#somethins more
			print "type1"

	def order_domain_value(type,node,nodes):
		#select the ordereing of the node based on the neighbours & their remaining domains!
		print "yp"

	

	def simple_backtrack(self,assignment,nodes):
		adj_matrix=self.adj_matrix
		if self.check_assignment(assignment):
			self.answer=assignment
			return assignment
		var = self.select_unassigned_var(0,nodes)	#selecting the node
		l=self.order_domain_value(0,var,nodes)	#Order in which to choose the nodes
		for value in l:
			new_nodes=copy.deepcopy(nodes)
			new_assignment=copy.deepcopy(assignment)
			if self.check_consistency(value,var,assignment):
				new_assignment=self.add_val(assignment,value,var)
				inference = self.inf(0,value,var,nodes)
				if inference:
					new_nodes=self.add_inference(0,new_nodes,inference)
					result=simple_backtrack(new_assignment,new_nodes)
					if result:
						return result


app = Flask(__name__, static_url_path='')
app.secret_key="secret"


@app.route("/",methods=['GET','POST'])		#Why some functions are called without being called. Just Calling them *************************************************
def home():
	if (request.method=='POST'):
		points=int(request.form['number'])
		density=int(request.form['density'])
		colours=int(request.form['color'])
		density=density/10.0
		print density
		algo=request.form['algo']
		local=request.form['local']
		g=graph(1500,770,density,points)
		g.add_points()
		g.add_edges()
		adj_matrix=g.adj_matrix()
		fo = open("input.txt", "wb")
		if algo!="local":
			fo.write(str(points)+" "+str(colours)+'\n');
		else:
			fo.write(str(points)+" "+str(colours)+" "+str(local)+'\n');
		for i in adj_matrix:
			for j in i:
				fo.write(str(j)+" ")
			fo.write("\n")
		fo.close()
		local_moves=0
		initial_time=time.time()
		if algo=="simple":
			#call(["g++","simple.cpp","-o","simple"])
			call(["./simple"])
		if algo=="forward":
			#call(["g++","forward.cpp","-o","forward"])
			call(["./forward"])
		if algo=="mac":
			#call(["g++","mac.cpp","-o","mac"])
			call(["./mac"])
		if algo=="local":
			#call(["g++","local.cpp","-o","local"])
			call(["./local"])
		final_time=time.time()
		file = open("output.txt", "r")
		ans=[]
		flag=0
		solvable=1 
		for line in file:
			#print line
			k=line.split(" ")
			if k[0]=="not_solvable":
				solvable=0
				break
			if algo=="local" and flag==0:
				local_moves=k[0]
				flag=1
				continue
			int_list = [int(i) for i in k]
			ans.append(int_list)
		for a in ans:
			a.append(g.points[a[0]].x)
			a.append(g.points[a[0]].y)
		file.close()
		print ans
		#print local_moves
		if local_moves=="-1\n":
			solvable=0
		running_time=final_time-initial_time
		#print local_moves
		return render_template('map.html',points=g.points,type=algo,edges=g.edges,ans=ans,solvable=solvable,running_time=running_time,local_moves=local_moves)
	return render_template('index.html')










if __name__ == "__main__":
	app.run(debug=True)