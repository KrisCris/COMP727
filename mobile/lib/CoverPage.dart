import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:qrscan/qrscan.dart' as scanner;
import 'package:web_socket_channel/io.dart';
import 'package:web_socket_channel/web_socket_channel.dart';

class CoverPage extends StatefulWidget {
  @override
  State<StatefulWidget> createState() {
    return CoverState();
  }
}

class CoverState extends State<CoverPage> {
  Widget getPage(String text) {
    return Container(
      decoration: BoxDecoration(color: Colors.white),
      child: ClipRRect(
          // make sure we apply clip it properly
          child: Container(
              alignment: Alignment.center,
              color: Colors.white,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.center,
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(FontAwesomeIcons.smileWink,
                      color: Colors.black, size: 50),
                  SizedBox(height: 30),
                  Text("Monitor you working and rest stat",
                      textDirection: TextDirection.ltr,
                      textAlign: TextAlign.center,
                      style: TextStyle(
                          decoration: TextDecoration.none,
                          fontSize: 22,
                          fontWeight: FontWeight.bold,
                          fontFamily: "Futura",
                          color: Colors.black)),
                  SizedBox(height: 50),
                  Text(text,
                      textDirection: TextDirection.ltr,
                      textAlign: TextAlign.center,
                      style: TextStyle(
                          decoration: TextDecoration.none,
                          fontSize: 13,
                          fontWeight: FontWeight.bold,
                          fontFamily: "Futura",
                          color: Colors.black))
                ],
              ))),
    );
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder(
        future: scanner.scan(),
        builder: (context, snapShot) {
          if(snapShot.hasData){
            String link = snapShot.data;
            WebSocketChannel c = new IOWebSocketChannel.connect('ws://$link:5050/mobile');
            c.sink.add('try to connect!');
            Future.delayed(Duration(milliseconds: 2500), () {
              Navigator.of(context)
                  .popAndPushNamed('/main', arguments: c);
            });
          } else {

          }

          return this.getPage("Connecting!");
        });
  }
}
