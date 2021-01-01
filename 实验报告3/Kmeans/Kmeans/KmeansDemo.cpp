// Kmeans.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include "pch.h"
#include <iostream>
#include<stdio.h>
#include<stdlib.h>
#include <fstream>
#include "kMeans.h"
using namespace std;

#pragma warning(disable:4996)

#define N 11   //11列
#define L 100 //100行

const char file_name[50] = "d:\\data.txt";//数据源：文件路径

int main()
{
	//数据源------------------------------------------

	//1.数据源：文本文件
	//FILE *fp;
	//double data[N * L]= { 0.0 };   //一维数组
	//double temp;
	//int i, j;
	//int count = 0;  //计数器，记录已读出的浮点数
	//if ((fp = fopen(file_name, "rb")) == NULL) {
	//	printf("请确认文件(%s)是否存在!\n", file_name);
	//	exit(1);
	//}
	//while (1 == fscanf(fp, "%lf", &temp)) {
	//	if (count == L * N)break;
	//	data[count] = temp;

	//	/*Debug
	//	if (count %11 == 0)
	//		printf("\n");
	//	printf("%lf ", temp);
	//	*/
	//	count++;
	//}
	//
	//fclose(fp);
	//const int size = L; //Number of samples行数
	//const int dim = N;   //Dimension of feature列数

	//数据源2：数组
	double data[2 * 20] = {
		3.45,7.08,
		1.76,7.24,
		4.29,9.55,
		3.35,6.65,
		3.17,6.41,
		3.68,5.99,
		2.11,4.08,
		2.58,7.10,
		3.45,7.88,
		6.17,5.40,
		4.20,6.46,
		5.87,3.87,
		5.47,2.21,
		5.97,3.62,
		6.24,3.06,
		6.89,2.41,
		5.38,2.32,
		5.13,2.73,
		7.26,4.19,
		6.32,3.62
	};
	const int size = 20; //Number of samples行数
	const int dim = 2;   //Dimension of feature列数

	//数据源------------------------------------------
	
	const int cluster_num = 5; //K值: Cluster number

	KMeans* kmeans = new KMeans(dim, cluster_num);
	int* labels = new int[size];
	kmeans->SetInitMode(KMeans::InitUniform);

	double* maxDis = new double[size];//点到类中心的距离
	double center[size*dim] = {};

	kmeans->Cluster(data, size, labels, maxDis, center);
	
	printf("\nK = %d\n",cluster_num);
	for (int i = 0; i < size; ++i)
	{
		printf("数据：(%.2f,%.2f) 属于： %d cluster，dis：%f,center：(%f,%f)\n", data[i*dim + 0], data[i*dim + 1], labels[i], maxDis[i],center[i*dim+0], center[i*dim + 1]);
	}
	
	ofstream out("k=5.txt");//可改名字

	double test_x = 2;
	double test_y = 6;
	double test_dis = -1;
	int Class = -1;
	for (int i = 0; i < size; i++) {
		double temp = sqrt((test_x - center[i*dim + 0])*(test_x - center[i*dim + 0]) + (test_y - center[i*dim + 1])*(test_y - center[i*dim + 1]));
		if (test_dis < temp && test_dis != -1) {
			
		}
		else
		{
			Class = labels[i];
			test_dis = temp;
		}
	}
	cout << "(2,6)属于:"<<Class << endl;

	for (int i = 0; i < size; ++i)
	{
		out<<data[i*dim + 0]<<" "<<data[i*dim + 1] << " " <<labels[i] << " " <<maxDis[i] << " " <<center[i*dim + 0] << " " <<center[i*dim + 1]<<endl;
	}

	out.close();

	delete[] maxDis;
	delete[] labels;
	delete kmeans;
	
	return 0;
}