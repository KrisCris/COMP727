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
      onGenerateRoute: (RouteSettings settings){
        return MaterialPageRoute(builder: (context){
          String routeName = settings.name;

          print("genRoute: "+routeName);

          if(routeName == '/main'){
            return MainPage();
          } else {
            return CoverPage();
          }
        });
      },

      routes: {
        // "/dashboard": (context)=>Dashboard()
      },
    );
  }

}