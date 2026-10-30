import 'dart:async';
import 'dart:math';
import 'package:flutter/material.dart';

void main() => runApp(const PrimeHostApp());

class PrimeHostApp extends StatelessWidget {
  const PrimeHostApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark(useMaterial3: true).copyWith(scaffoldBackgroundColor: const Color(0xFF0C0816)),
      home: const BackgroundWrapper(child: MainNav()),
    );
  }
}

// === REAL LIVE BACKGROUND - STORM EDITION ===
class BackgroundWrapper extends StatefulWidget {
  final Widget child; const BackgroundWrapper({super.key, required this.child});
  @override State<BackgroundWrapper> createState() => _BackgroundWrapperState();
}
class _BackgroundWrapperState extends State<BackgroundWrapper> with TickerProviderStateMixin {
  late AnimationController _storm;
  late AnimationController _flash;
  late AnimationController _particles;
  @override void initState(){
    _storm = AnimationController(vsync: this, duration: const Duration(seconds: 8))..repeat();
    _flash = AnimationController(vsync: this, duration: const Duration(milliseconds: 3500))..repeat();
    _particles = AnimationController(vsync: this, duration: const Duration(seconds: 12))..repeat();
    super.initState();
  }
  @override void dispose(){ _storm.dispose(); _flash.dispose(); _particles.dispose(); super.dispose();}
  @override Widget build(BuildContext context){
    return Stack(children: [
      Container(color: const Color(0xFF0C0816)),
      AnimatedBuilder(animation: _storm, builder: (_,__) => Container(decoration: BoxDecoration(gradient: RadialGradient(center: Alignment(0.3+sin(_storm.value*2*pi)*0.3, -0.8), radius: 1.2+_storm.value*0.3, colors: [const Color(0xFF8B5CF6).withOpacity(0.25+0.1*sin(_storm.value*2*pi)), const Color(0xFF1A0B3A).withOpacity(0.15), Colors.transparent])))),
      AnimatedBuilder(animation: _particles, builder: (_,__) => CustomPaint(size: Size.infinite, painter: ParticlePainter(t: _particles.value))),
      AnimatedBuilder(animation: _flash, builder: (_,__) => CustomPaint(size: Size.infinite, painter: RealLightningPainter(t: _flash.value))),
      Container(decoration: BoxDecoration(gradient: LinearGradient(begin: Alignment.topCenter, end: Alignment.bottomCenter, colors: [Colors.transparent, const Color(0xFF0C0816).withOpacity(0.85)]))),
      widget.child,
    ]);
  }
}

class ParticlePainter extends CustomPainter {
  final double t; ParticlePainter({required this.t});
  @override void paint(Canvas c, Size s){
    final r = Random(42);
    final paint = Paint();
    for(int i=0;i<40;i++){
      double x = (r.nextDouble()*s.width + t*s.width*0.2) % s.width;
      double y = (r.nextDouble()*s.height + sin(t*2*pi + i)*30) % s.height;
      double sz = r.nextDouble()*2+0.5;
      paint.color = Color.lerp(const Color(0xFF8B5CF6), Colors.white, r.nextDouble()*0.5)!.withOpacity(0.1+r.nextDouble()*0.3);
      c.drawCircle(Offset(x,y), sz, paint);
    }
  }
  @override bool shouldRepaint(covariant ParticlePainter old)=>true;
}

class RealLightningPainter extends CustomPainter {
  final double t; RealLightningPainter({required this.t});
  @override void paint(Canvas canvas, Size size){
    final rand = Random(123);
    double flashChance = sin(t*2*pi*1.7).abs();
    if(flashChance>0.92){
      final flashPaint = Paint()..color=Colors.white.withOpacity((flashChance-0.92)*3)..style=PaintingStyle.fill;
      canvas.drawRect(Rect.fromLTWH(0,0,size.width,size.height), flashPaint);
    }
    for(int b=0;b<2;b++){
      if(rand.nextDouble()>0.6) continue;
      double startX = rand.nextDouble()*size.width;
      double startY = -10;
      double endX = startX + (rand.nextDouble()-0.5)*200;
      double endY = size.height*0.7 + rand.nextDouble()*200;
      _drawBolt(canvas, Offset(startX, startY), Offset(endX, endY), rand, mainColor: const Color(0xFFA78BFA), glow: true);
      if(rand.nextBool()){
        _drawBolt(canvas, Offset(startX*0.6+endX*0.4, startY*0.3+endY*0.7), Offset(endX+rand.nextDouble()*100-50, endY+50), rand, mainColor: const Color(0xFF8B5CF6).withOpacity(0.6), glow:false, width:0.8);
      }
    }
  }
  void _drawBolt(Canvas canvas, Offset start, Offset end, Random rand, {required Color mainColor, required bool glow, double width=1.5}){
    final path = Path()..moveTo(start.dx, start.dy);
    double x=start.dx, y=start.dy;
    int segments = 18;
    for(int i=0;i<segments;i++){
      double progress = (i+1)/segments;
      double targetX = start.dx + (end.dx-start.dx)*progress;
      double targetY = start.dy + (end.dy-start.dy)*progress;
      x = targetX + (rand.nextDouble()-0.5)*30;
      y = targetY + (rand.nextDouble()-0.5)*10;
      path.lineTo(x,y);
    }
    if(glow){
      final glowPaint = Paint()..color=mainColor.withOpacity(0.15)..strokeWidth=width+6..style=PaintingStyle.stroke..maskFilter=const MaskFilter.blur(BlurStyle.normal, 8);
      canvas.drawPath(path, glowPaint);
    }
    final paint = Paint()..color=mainColor..strokeWidth=width..style=PaintingStyle.stroke..strokeCap=StrokeCap.round;
    canvas.drawPath(path, paint);
    final corePaint = Paint()..color=Colors.white.withOpacity(0.8)..strokeWidth=width*0.4..style=PaintingStyle.stroke;
    canvas.drawPath(path, corePaint);
  }
  @override bool shouldRepaint(covariant RealLightningPainter old)=>true;
}

// LIVE REAL TIME
class LiveClock extends StatefulWidget { const LiveClock({super.key}); @override State<LiveClock> createState()=>_LiveClockState();}
class _LiveClockState extends State<LiveClock> { late Timer timer; DateTime now=DateTime.now(); @override void initState(){ timer=Timer.periodic(const Duration(seconds:1), (_)=> setState(()=> now=DateTime.now())); super.initState();} @override void dispose(){ timer.cancel(); super.dispose();} @override Widget build(BuildContext context){ return Text("${now.toLocal().toString().split('.')[0]}", style: const TextStyle(color: Colors.white38, fontSize: 11)); }}

class MainNav extends StatefulWidget {
  const MainNav({super.key});
  @override
  State<MainNav> createState() => _MainNavState();
}

class _MainNavState extends State<MainNav> {
  int idx = 0;
  final screens = [const HomeScreen(), const MetatraderScreen(), const ScannerScreen(), const SettingsScreen()];
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.transparent,
      body: screens[idx],
      bottomNavigationBar: BottomNavigationBar(
        backgroundColor: const Color(0xFF140E26),
        type: BottomNavigationBarType.fixed,
        currentIndex: idx,
        onTap: (i) => setState(() => idx = i),
        selectedItemColor: const Color(0xFF8B5CF6),
        unselectedItemColor: Colors.white38,
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home_outlined), label: "Home"),
          BottomNavigationBarItem(icon: Icon(Icons.desktop_windows_outlined), label: "Metatrader"),
          BottomNavigationBarItem(icon: Icon(Icons.psychology_outlined), label: "Scanner"),
          BottomNavigationBarItem(icon: Icon(Icons.settings_outlined), label: "Settings"),
        ],
      ),
    );
  }
}

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});
  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Center(child: LiveClock()),
            const SizedBox(height: 12),
            Container(
              height: 360,
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(24),
                border: Border.all(color: const Color(0xFF3A2A60)),
                gradient: const LinearGradient(colors: [Color(0xFF2A1F45), Color(0xFF0C0816)]),
              ),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.end,
                children: [
                  const Icon(Icons.memory, size: 100, color: Color(0xFF8B5CF6)),
                  const SizedBox(height: 20),
                  const Text("KAYVIEW CHARGER", style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 22, letterSpacing: 1)),
                  const SizedBox(height: 8),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
                    decoration: BoxDecoration(borderRadius: BorderRadius.circular(20), border: Border.all(color: Color(0xFF8B5CF6)), color: Color(0xFF1E1635)),
                    child: const Text("Powered By Ambient", style: TextStyle(color: Colors.white, fontSize: 12)),
                  ),
                  const SizedBox(height: 20),
                ],
              ),
            ),
            const SizedBox(height: 14),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
              decoration: BoxDecoration(borderRadius: BorderRadius.circular(30), border: Border.all(color: const Color(0xFF8B5CF6)), color: const Color(0xFF1A1430)),
              child: const Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  Row(children: [Icon(Icons.close, size: 18, color: Color(0xFF8B5CF6)), SizedBox(width: 6), Text("Remove", style: TextStyle(color: Colors.white, fontSize: 13))]),
                  Row(children: [Icon(Icons.play_arrow, size: 18, color: Color(0xFF8B5CF6)), SizedBox(width: 6), Text("Start", style: TextStyle(color: Colors.white, fontSize: 13))]),
                  Row(children: [Icon(Icons.bar_chart, size: 18, color: Color(0xFF8B5CF6)), SizedBox(width: 6), Text("Symbols", style: TextStyle(color: Colors.white, fontSize: 13))]),
                ],
              ),
            ),
            const SizedBox(height: 20),
            const Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text("ROBOT LIST", style: TextStyle(color: Colors.white38, fontSize: 13)),
                Text("+ Add Key", style: TextStyle(color: Color(0xFF8B5CF6), fontSize: 13, fontWeight: FontWeight.bold)),
              ],
            ),
            const SizedBox(height: 10),
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(borderRadius: BorderRadius.circular(30), border: Border.all(color: const Color(0xFF8B5CF6)), color: const Color(0xFF1A1430)),
              child: Row(
                children: [
                  const CircleAvatar(backgroundColor: Color(0xFF2A1F45), radius: 22, child: Icon(Icons.memory, color: Colors.white38)),
                  const SizedBox(width: 12),
                  const Expanded(
                    child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                      Text("KAYVIEW CHARGER", style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 13)),
                      Text("PHE••••E78", style: TextStyle(color: Colors.white38, fontSize: 11)),
                      Text("Key expires in 361d 15h", style: TextStyle(color: Color(0xFF8B5CF6), fontSize: 10)),
                    ]),
                  ),
                  Container(padding: const EdgeInsets.all(8), decoration: BoxDecoration(color: const Color(0xFF2A1F45), borderRadius: BorderRadius.circular(20)), child: const Icon(Icons.delete_outline, size: 18, color: Colors.white38)),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class MetatraderScreen extends StatelessWidget {
  const MetatraderScreen({super.key});
  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            Container(width: double.infinity, padding: const EdgeInsets.symmetric(vertical: 12), decoration: BoxDecoration(borderRadius: BorderRadius.circular(30), border: Border.all(color: const Color(0xFF8B5CF6)), color: const Color(0xFF140E26)), child: const Center(child: Text("MT5 ACCOUNT", style: TextStyle(color: Color(0xFF8B5CF6), fontWeight: FontWeight.bold)))),
            const SizedBox(height: 16),
            Row(mainAxisAlignment: MainAxisAlignment.center, children: [Container(width: 10, height: 10, decoration: BoxDecoration(color: Colors.red, borderRadius: BorderRadius.circular(10))), const SizedBox(width: 8), const Text("MT5 DISCONNECTED", style: TextStyle(color: Colors.white54, fontSize: 12))]),
            const SizedBox(height: 24),
            Container(height: 180, decoration: BoxDecoration(borderRadius: BorderRadius.circular(20), border: Border.all(color: const Color(0xFFC5A86A)), gradient: const LinearGradient(colors: [Color(0xFF2B2B2B), Color(0xFF0F0F0F)])), child: const Padding(padding: EdgeInsets.all(16), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [Text("KC  KAYVIEW CHARGER", style: TextStyle(color: Color(0xFFC5A86A), fontWeight: FontWeight.bold, fontSize: 16)), Spacer(), Text("TAP TO FLIP", style: TextStyle(color: Colors.white24, fontSize: 9))] ))),
            const SizedBox(height: 20),
            const Text("MT5 LOGIN DETAILS", style: TextStyle(fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            const Row(children: [Expanded(child: _Tab(active: true, t: "CONNECT ACCOUNT")), SizedBox(width: 10), Expanded(child: _Tab(active: false, t: "ORDERS"))]),
            const SizedBox(height: 16),
            _input("Login"),
            const SizedBox(height: 12),
            _input("Password", isPass: true),
            const SizedBox(height: 12),
            _input("Server", isServer: true),
          ],
        ),
      ),
    );
  }
  static Widget _input(String hint, {bool isPass = false, bool isServer = false}) {
    return Container(
      decoration: BoxDecoration(borderRadius: BorderRadius.circular(20), border: Border.all(color: const Color(0xFF8B5CF6)), color: const Color(0xFF1A1A1A)),
      child: TextField(obscureText: isPass, decoration: InputDecoration(hintText: hint, hintStyle: const TextStyle(color: Colors.white24), border: InputBorder.none, contentPadding: const EdgeInsets.symmetric(horizontal: 18, vertical: 16), suffixIcon: isPass || isServer ? Container(margin: const EdgeInsets.all(4), decoration: BoxDecoration(color: const Color(0xFF2A2A2A), borderRadius: BorderRadius.circular(14)), child: Icon(isPass ? Icons.visibility_outlined : Icons.close, color: const Color(0xFF8B5CF6), size: 18)) : null)),
    );
  }
}

class _Tab extends StatelessWidget {
  final bool active; final String t;
  const _Tab({required this.active, required this.t});
  @override
  Widget build(BuildContext context) {
    return Container(padding: const EdgeInsets.symmetric(vertical: 14), decoration: BoxDecoration(borderRadius: BorderRadius.circular(12), color: active ? const Color(0xFF2A1A4A) : const Color(0xFF1A1A1A), border: Border.all(color: active ? const Color(0xFF8B5CF6) : Colors.white10)), child: Center(child: Text(t, style: TextStyle(color: active ? const Color(0xFF8B5CF6) : Colors.white38, fontSize: 12, fontWeight: FontWeight.bold))));
  }
}

class ScannerScreen extends StatelessWidget {
  const ScannerScreen({super.key});
  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            const SizedBox(height: 10),
            Container(width: 80, height: 80, decoration: BoxDecoration(shape: BoxShape.circle, border: Border.all(color: const Color(0xFF8B5CF6))), child: const Center(child: Text("A", style: TextStyle(fontSize: 30, fontWeight: FontWeight.bold)))),
            const SizedBox(height: 16),
            const Text("AI Analysis", style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const Text("SNIPER ELITE · ENTRY HUNTER", style: TextStyle(color: Colors.white38, fontSize: 11)),
            const SizedBox(height: 12),
            const Text("1. Pick pair & timeframe\n2. Watch the live chart & ask/bid\n3. Tap Analyse to fire the sniper", textAlign: TextAlign.center, style: TextStyle(color: Colors.white54, fontSize: 12)),
            const SizedBox(height: 16),
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(borderRadius: BorderRadius.circular(20), color: const Color(0xFF1A1030), border: Border.all(color: Colors.white10)),
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                const Text("PAIR (PICK)", style: TextStyle(color: Colors.white38, fontSize: 11)),
                const SizedBox(height: 6),
                _dropdown("XAUUSD"),
                const SizedBox(height: 12),
                const Text("TIMEFRAME", style: TextStyle(color: Colors.white38, fontSize: 11)),
                const SizedBox(height: 6),
                _dropdown("M15"),
                const SizedBox(height: 16),
                Container(padding: const EdgeInsets.all(12), decoration: BoxDecoration(borderRadius: BorderRadius.circular(16), color: const Color(0xFF0C0816), border: Border.all(color: Colors.white10)), child: Column(children: [
                  const Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [Column(crossAxisAlignment: CrossAxisAlignment.start, children: [Text("LIVE QUOTE", style: TextStyle(color: Colors.white38, fontSize: 10)), Text("XAUUSD", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16))]), Text("Fetching...", style: TextStyle(color: Colors.white54, fontSize: 11))]),
                  const SizedBox(height: 12),
                  const Row(children: [
                    Expanded(child: _BidAsk(color: Colors.red, label: "BID")),
                    SizedBox(width: 10),
                    Expanded(child: _BidAsk(color: Colors.green, label: "ASK")),
                  ]),
                ])),
              ]),
            ),
          ],
        ),
      ),
    );
  }
  static Widget _dropdown(String val) => Container(padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12), decoration: BoxDecoration(borderRadius: BorderRadius.circular(12), color: const Color(0xFF2A2A2A), border: Border.all(color: Colors.white24)), child: Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [Text(val, style: const TextStyle(fontWeight: FontWeight.bold)), const Icon(Icons.keyboard_arrow_down, color: Colors.white54)]));
}

class _BidAsk extends StatelessWidget {
  final Color color; final String label;
  const _BidAsk({required this.color, required this.label});
  @override
  Widget build(BuildContext context) {
    return Container(padding: const EdgeInsets.symmetric(vertical: 14), decoration: BoxDecoration(borderRadius: BorderRadius.circular(14), border: Border.all(color: color)), child: Column(children: [Text(label, style: TextStyle(color: color, fontSize: 11, fontWeight: FontWeight.bold)), const Text("--", style: TextStyle(fontWeight: FontWeight.bold))]));
  }
}

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});
  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: const [
          Text("Settings", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
          SizedBox(height: 12),
          _SetCard(title: "FONT", value: "Space Grotesk"),
          _SetCard(title: "THEME", value: "Purple"),
          _SetCard(title: "BACKGROUND EFFECT", value: "Lightning - LIVE"),
          _SetCard(title: "AI STRATEGY", value: "Auto - Full confluence stack"),
          _SetCard(title: "PRIME HOST EA - VOICE CONTROL", value: "Off"),
        ],
      ),
    );
  }
}

class _SetCard extends StatelessWidget {
  final String title, value;
  const _SetCard({required this.title, required this.value});
  @override
  Widget build(BuildContext context) {
    return Container(margin: const EdgeInsets.only(bottom: 12), padding: const EdgeInsets.all(14), decoration: BoxDecoration(borderRadius: BorderRadius.circular(16), color: const Color(0xFF1E1040), border: Border.all(color: Colors.white10)), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [Text(title, style: const TextStyle(color: Colors.white38, fontSize: 10)), Text(value, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13))]));
  }
}
