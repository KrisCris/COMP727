import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'MainPage.dart';
import 'CoverPage.dart';

void main(){
  runApp(App());
}

class App extends StatelessWidget{
  BuildContext context;

  @override
  Widget build(BuildContext context) {
    this.context = context;

    return MaterialApp(
      home: new CoverPage(),
      routes: {
        "/main": (context)=>MainPage(ModalRoute.of(context).settings.arguments)
      },
    );
  }

}