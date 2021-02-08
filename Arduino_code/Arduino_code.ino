//Teste - Acender Led
int led = 7;
int led2 = 6;
int led3 = 5;
int ldr = A1;
int LM35 = A2;
char ch;

void setup() {
    Serial.begin(9600);
    pinMode(led, OUTPUT);
    pinMode(led2, OUTPUT);
    pinMode(led3, OUTPUT);
    pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  if (Serial.available())
  {
    ch = Serial.read();
    Serial.println(ch);

    if (ch == '1')
    {
      if (digitalRead(led) == HIGH)
      {
        digitalWrite(led, LOW);
      }
      else
      {
        digitalWrite(led, HIGH);
      }

      if (digitalRead(LED_BUILTIN) == HIGH)
      {
        digitalWrite(LED_BUILTIN, LOW);
      }
      else
      {
        digitalWrite(LED_BUILTIN, HIGH);
      }
    }

    else if (ch == '2')
    {
      if (digitalRead(led2) == HIGH)
      {
        digitalWrite(led2, LOW);
      }
      else
      {
        digitalWrite(led2, HIGH);
      }
    }

    else if (ch == '3')
    {
      if (digitalRead(led3) == HIGH)
      {
        digitalWrite(led3, LOW);
      }
      else
      {
        digitalWrite(led3, HIGH);
      }
    }
  }
  delay(200);

  int lumin = analogRead(ldr);//Luminosidade
  int temp = analogRead(LM35);//Temperatura
  Serial.print('L');
  Serial.print(lumin);
  Serial.print('T');
  Serial.println(temp);
}
