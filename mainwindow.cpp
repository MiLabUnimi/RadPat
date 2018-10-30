#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <iostream>
#include <QStringList>
#include <QPalette>
#include <QFileDialog>
#include <QtCharts/QChart>
#include <QtCharts/QScatterSeries>
#include <QtCharts/QLineSeries>
#include <QtCharts/QSplineSeries>
#include <QtCharts/QValueAxis>
#include <QtCharts/QChartView>
#include <QGridLayout>


using namespace QtCharts;





MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{

    ui->setupUi(this);
    QScatterSeries *measure = new QScatterSeries();
    QChart *chartl;
    QChartView *view;
    chartl = new QChart();
    view = new QChartView();


    measure->setName("Radiation Pattern");
    for (int i = -90; i <= 90; i += 10) measure->append(i, i);

    chartl->addSeries(measure);
    chartl->createDefaultAxes();
    measure->clear();
    view->setChart(chartl);

    view->setRenderHint(QPainter::Antialiasing);
    view->resize(ui->tableChart->size());

    QGridLayout lay_chart;
    lay_chart.addWidget(view);
    ui->tableChart->setLayout(&lay_chart);






}

MainWindow::~MainWindow()
{
    delete ui;
}
