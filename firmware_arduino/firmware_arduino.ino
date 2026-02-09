#define CLK 2
#define DT 3
#define SW 4

int counter = 0; // posizione in gradi: da -180 a +180
int currentStateCLK;
int lastStateCLK;

// ========================
// SETUP
// ========================
void setup() {
  pinMode(CLK, INPUT);
  pinMode(DT, INPUT);
  pinMode(SW, INPUT_PULLUP);

  Serial.begin(9600);
  lastStateCLK = digitalRead(CLK);

  Serial.println("Rotary + Serial Protocol Ready");
}

// ========================
// LOOP PRINCIPALE
// ========================
void loop() {
  gestisciEncoder();
  gestisciSeriale();
}

// ========================
// GESTIONE ENCODER
// ========================
void gestisciEncoder() {
  currentStateCLK = digitalRead(CLK);

  if (currentStateCLK != lastStateCLK) {
    if (digitalRead(DT) != currentStateCLK) {
      if (counter < 180) counter++;
    } else {
      if (counter > -180) counter--;
    }

    Serial.print("POS=");
    Serial.println(counter);
  }

  lastStateCLK = currentStateCLK;

  // Pulsante
  if (digitalRead(SW) == LOW) {
    Serial.println("BTN");
    delay(200);
  }
}

// ========================
// GESTIONE PROTOCOLLO SERIALE
// ========================
void gestisciSeriale() {
  if (!Serial.available()) return;

  String cmd = Serial.readStringUntil('\n');
  cmd.trim();

  // ========================================
  // COMANDO: STOP
  // ========================================
  if (cmd == "STOP") {
    Serial.println("OK STOP");
    return;
  }

  // ========================================
  // COMANDO: RESET
  // ========================================
  if (cmd == "RESET") {
    counter = 0;
    Serial.println("OK RESET");
    return;
  }

  // ========================================
  // COMANDO: OC (open/close della cupola)
  // ========================================
  if (cmd == "OC") {
    Serial.println("OK OC");
    return;
  }

  // ========================================
  // COMANDO: CW;VAL
  // ========================================
  if (cmd.startsWith("CW;")) {
    int gradi = cmd.substring(3).toInt();
    if (gradi <= 0 || gradi > 180) {
      Serial.println("ERR");
      return;
    }

    counter += gradi;
    if (counter > 180) counter = 180;

    Serial.print("OK CW ");
    Serial.println(counter);
    return;
  }

  // ========================================
  // COMANDO: CCW;VAL
  // ========================================
  if (cmd.startsWith("CCW;")) {
    int gradi = cmd.substring(4).toInt();
    if (gradi <= 0 || gradi > 180) {
      Serial.println("ERR");
      return;
    }

    counter -= gradi;
    if (counter < -180) counter = -180;

    Serial.print("OK CCW ");
    Serial.println(counter);
    return;
  }

  // ========================================
  // COMANDO: POS
  // ========================================
  if (cmd == "POS") {
    Serial.print("POS;");
    Serial.println(counter);
    return;
  }

  // Se non corrisponde a nulla:
  Serial.println("ERR CMD");
}