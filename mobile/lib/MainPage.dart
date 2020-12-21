import 'dart:collection';

import 'package:flutter/material.dart';
import 'package:flutter_staggered_grid_view/flutter_staggered_grid_view.dart';
import 'package:web_socket_channel/io.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:syncfusion_flutter_charts/charts.dart';
import 'dart:convert';

class MainPage extends StatefulWidget {
  final String title = 'SmartReminder';
  WebSocketChannel channel;

  MainPage(WebSocketChannel c){
    // this.channel = new IOWebSocketChannel.connect('ws://$link:5050/mobile');
    this.channel = c;
  }

  @override
  _MainPageState createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {
  List<List<double>> charts = [
    [6],
    [6],
    [6],
    [6]
  ];

  static final List<String> chartDropdownItems = [
    'Last 1 Hour',
    'Last 3 Hour',
    'Last 6 Hour',
    'Last 12 Hour'
  ];
  String actualDropdown = chartDropdownItems[0];
  int actualChart = 0;

  double workingHour = 0;
  double temperature = 0;
  double humidity = 0;
  List<WorkingData> workingData = [];
  List<List<EmotionData>> emotionData = [[],[],[],[]];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          elevation: 2.0,
          backgroundColor: Colors.white,
          title: Text(widget.title,
              style: TextStyle(
                  color: Colors.black,
                  fontWeight: FontWeight.w700,
                  fontSize: 30.0)),
        ),
        body: new StreamBuilder(
            stream: widget.channel.stream,
            builder: (context, snapshot) {
              if (!snapshot.hasData) {
                widget.channel.sink.add('mobile');
              }
              if (snapshot.hasData) {
                String str = snapshot.data.toString().replaceAll("'", '"');
                Map<String, dynamic> data = jsonDecode(str);
                this.temperature = data['tmp'];
                this.humidity = data['hmd'];
                this.workingHour = data['worktime'];
                for(int i = 0; i < 4; i++){
                  Map<String,int> emap = new Map.from(data['edata'][i]);
                  this.emotionData[i].clear();
                  emap.forEach((key, value) {
                    this.emotionData[i].add(EmotionData(key, value));
                  });
                }

                Map<String,int> wmap = new Map.from(data['wdata']);
                this.workingData.clear();
                wmap.forEach((key, value) {
                  this.workingData.add(WorkingData(key, value));
                });
              }

              return StaggeredGridView.count(
                crossAxisCount: 2,
                crossAxisSpacing: 12.0,
                mainAxisSpacing: 12.0,
                padding: EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
                children: <Widget>[
                  _buildTile(
                    Padding(
                      padding: const EdgeInsets.all(24.0),
                      child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          crossAxisAlignment: CrossAxisAlignment.center,
                          children: <Widget>[
                            Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: <Widget>[
                                Text("Today's Working Hour",
                                    style: TextStyle(color: Colors.blueAccent)),
                                Text(workingHour.toStringAsFixed(1) + 'h',
                                    style: TextStyle(
                                        color: Colors.black,
                                        fontWeight: FontWeight.w700,
                                        fontSize: 34.0))
                              ],
                            ),
                            Material(
                                color: Colors.blue,
                                borderRadius: BorderRadius.circular(24.0),
                                child: Center(
                                    child: Padding(
                                  padding: const EdgeInsets.all(16.0),
                                  child: Icon(Icons.work,
                                      color: Colors.white, size: 30.0),
                                )))
                          ]),
                    ),
                  ),
                  _buildTile(
                    Padding(
                      padding: const EdgeInsets.all(24.0),
                      child: Column(
                          mainAxisAlignment: MainAxisAlignment.start,
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: <Widget>[
                            Material(
                                color: Colors.teal,
                                shape: CircleBorder(),
                                child: Padding(
                                  padding: const EdgeInsets.all(16.0),
                                  child: Icon(FontAwesomeIcons.temperatureLow,
                                      color: Colors.white, size: 30.0),
                                )),
                            Padding(padding: EdgeInsets.only(bottom: 16.0)),
                            Text(temperature.toString() + '°C',
                                style: TextStyle(
                                    color: Colors.black,
                                    fontWeight: FontWeight.w700,
                                    fontSize: 30.0)),
                          ]),
                    ),
                  ),
                  _buildTile(
                    Padding(
                      padding: const EdgeInsets.all(24.0),
                      child: Column(
                          mainAxisAlignment: MainAxisAlignment.start,
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: <Widget>[
                            Material(
                                color: Colors.amber,
                                shape: CircleBorder(),
                                child: Padding(
                                  padding: EdgeInsets.all(16.0),
                                  child: Icon(FontAwesomeIcons.tint,
                                      color: Colors.white, size: 30.0),
                                )),
                            Padding(padding: EdgeInsets.only(bottom: 16.0)),
                            Text(humidity.toStringAsFixed(0) + '%',
                                style: TextStyle(
                                    color: Colors.black,
                                    fontWeight: FontWeight.w700,
                                    fontSize: 30.0)),
                          ]),
                    ),
                  ),
                  _buildTile(
                    Padding(
                        padding: const EdgeInsets.all(24.0),
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.start,
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: <Widget>[
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: <Widget>[
                                Column(
                                  mainAxisAlignment: MainAxisAlignment.start,
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: <Widget>[
                                    Text('Happiness (Higher the better)',
                                        style: TextStyle(color: Colors.green)),
                                  ],
                                ),
                                DropdownButton(
                                    isDense: true,
                                    value: actualDropdown,
                                    onChanged: (String value) => setState(() {
                                          actualDropdown = value;
                                          actualChart =
                                              chartDropdownItems.indexOf(
                                                  value); // Refresh the chart
                                        }),
                                    items:
                                        chartDropdownItems.map((String title) {
                                      return DropdownMenuItem(
                                        value: title,
                                        child: Text(title,
                                            style: TextStyle(
                                                color: Colors.blue,
                                                fontWeight: FontWeight.w400,
                                                fontSize: 14.0)),
                                      );
                                    }).toList())
                              ],
                            ),
                            Padding(padding: EdgeInsets.only(bottom: 4.0)),
                            // Sparkline(
                            //   data: this.charts[this.actualChart],
                            //   lineWidth: 3.0,
                            //   lineColor: Colors.greenAccent,
                            // )
                            SfCartesianChart(
                              // Initialize category axis
                                primaryXAxis: CategoryAxis(),
                                primaryYAxis: NumericAxis(),
                                palette: [Colors.greenAccent],
                                series: <LineSeries<EmotionData, String>>[
                                  LineSeries<EmotionData, String>(
                                    // Bind data source
                                      dataSource:  this.emotionData[this.actualChart],
                                      xValueMapper: (EmotionData e, _) => e.time,
                                      yValueMapper: (EmotionData e, _) => e.stat,
                                  )
                                ]
                            )
                          ],
                        )),
                  ),
                  _buildTile(
                    Padding(
                        padding: const EdgeInsets.all(24.0),
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.start,
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: <Widget>[
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: <Widget>[
                                Column(
                                  mainAxisAlignment: MainAxisAlignment.start,
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: <Widget>[
                                    Text('Working Duration (Mins)',
                                        style:
                                            TextStyle(color: Colors.redAccent)),
                                    Text('',
                                        style: TextStyle(
                                            color: Colors.black,
                                            fontWeight: FontWeight.w700,
                                            fontSize: 15.0)),
                                  ],
                                ),
                              ],
                            ),
                            SfCartesianChart(
                                primaryXAxis: CategoryAxis(),
                                palette: [Colors.orangeAccent],
                                series: <BarSeries<WorkingData, String>>[
                                  BarSeries<WorkingData, String>(
                                      // Bind data source
                                      dataSource: this.workingData,
                                      xValueMapper: (WorkingData work, _) =>
                                          work.time,
                                      yValueMapper: (WorkingData work, _) =>
                                          work.hours)
                                ])
                          ],
                        )),
                  ),
                ],
                staggeredTiles: [
                  StaggeredTile.extent(2, 110.0),
                  StaggeredTile.extent(1, 180.0),
                  StaggeredTile.extent(1, 180.0),
                  StaggeredTile.extent(2, 382.0),
                  StaggeredTile.extent(2, 382),
                ],
              );
            }));
  }

  Widget _buildTile(Widget child, {Function() onTap}) {
    return Material(
        elevation: 14.0,
        borderRadius: BorderRadius.circular(12.0),
        shadowColor: Color(0x802196F3),
        child: InkWell(
            // Do onTap() if it isn't null, otherwise do print()
            onTap: onTap != null
                ? () => onTap()
                : () {
                    print('Not set yet');
                  },
            child: child));
  }

  @override
  void dispose() {
    widget.channel.sink.close();
    super.dispose();
  }
}

class WorkingData {
  WorkingData(this.time, this.hours);
  final String time;
  final int hours;
}

class EmotionData {
  EmotionData(this.time, this.stat);
  final String time;
  final int stat;
}