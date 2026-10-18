# Ocena początkowa i droga do benchmarku

Stan startowy: **skuteczność narzędzia niezmierzona, benchmark nie istnieje**.
Temat setupu przygotowuje ocenę; nie buduje produktu ani docelowego zestawu przypadków.
Podstawą są ustalenia [niezależnej weryfikacji](https://github.com/Kucze3205/ConnectWithLabview/issues/10#issuecomment-6225343449)
i [dostępu do środowiska](https://github.com/Kucze3205/ConnectWithLabview/issues/2#issuecomment-6248028771).
Kompilacja przykładu VI z 2014 w kontenerze NI 2026 Q1 dowodzi dostępu do tego środowiska,
nie poprawności czytnika, VI Scripting ani obsługi wszystkich wersji. Dostęp 2024 pozostaje niezweryfikowany.

## Co rozstrzyga skrypt, a co właściciel

Zachowano dostarczoną bramkę `gate.kind: owner`. Każda zmiana pracy czeka na decyzję
właściciela; nie zaakceptowano progów jakości ani samodzielnego kończenia celu.
Właściciel ocenia treść dowodów, dopuszcza rozpoczęcie implementacji dopiero po wiarygodnej
metodzie weryfikacji, akceptuje kryteria sukcesu i ewentualną zmianę zakresu. Zastąpienie
bramki skryptem wymaga jego decyzji oraz niezależnie sprawdzonej metody. Nie jest to
ograniczenie celu do wersji lub rodzin obecnych w pierwszych przykładach.

`check` uruchamia `python3 policy/evaluator/evaluate.py --check` w kandydacie. Sprawdza
jedynie poprawność opcjonalnego indeksu dowodów: schemat, lokalne ścieżki, niepuste pliki
i SHA256. Brak indeksu jest normalnym stanem początkowym, raportowanym jawnie; błędny
istniejący indeks zatrzymuje zmianę. Ten check nie potwierdza treści dokumentów ani jakości.
Nie wykonuje kodu wskazanego w dowodach. Testy tego skryptu i silnika nie są benchmarkiem LabVIEW.

Raport porównawczy uruchamia się z **zaakceptowanego drzewa**, podając oba katalogi:

```sh
python3 policy/evaluator/evaluate.py --baseline /accepted --candidate /candidate
```

Obsługiwane są też `BASELINE_DIR` i `CANDIDATE_DIR`. Ostatnia linia to JSON zgodny z
kontraktem silnika. Raport zawiera oba stany; błędne dowody kandydata dają `rejected`,
pozostałe przypadki `inconclusive`, zawsze `improved: false`. Nawet komplet odnośników
nie oznacza gotowości benchmarku. `tool_quality: null`, `benchmark_executed: false` oraz
`benchmark_ready: false` pozostają jawne. Raport jest pomocą dla właściciela; przy bramce
`owner` silnik nie uruchamia go automatycznie i nie wykorzystuje go do automatycznego przyjęcia.
Brak pomiaru pozostaje brakiem pomiaru, także po usunięciu lub wymianie indeksu.

Indeks `benchmark/preparation.json` powstanie podczas pracy pętli. Wzór, nie gotowy benchmark:

```json
{"schema_version":1,"milestones":{"sources":[],"tasks":[],"oracle":[],"split":[],"coverage":[],"baseline":[],"challenges":[]}}
```

Każda lista zawiera wpisy `{"path":"benchmark/protocol.md","sha256":"<64 znaki SHA256>"}`.
Dowody muszą być plikami w drzewie, bez symlinków, do 2 MB każdy; duże dane opisuje mały
rekord z przypiętym źródłem i hashem. Sekcje i liczba odnośników służą nawigacji, nie punktacji.
Check działa tylko dla zmian pracy; ścieżki polityki/audytu/dziennika omijają go zgodnie
z silnikiem. Weryfikator sam uruchamia testy każdej zmiany evaluatora.

## Co musi powstać przed implementacją

Pętla przygotuje następujące dowody, następnie niezależny weryfikator sprawdzi metodę,
a właściciel oceni jej wiarygodność przed przyjęciem implementacji. Nie wystarczy utworzyć pliki.

| Obszar | Wymagane ustalenia i dowody |
|---|---|
| sources | Pochodzenie, licencja, commit i SHA256 oryginałów; zależności, wersja zapisu artefaktu i wersja środowiska odczytu osobno. Zachować oryginał przed konwersją. |
| tasks | Zadania o przepływie danych, typach, strukturach, zależnościach, projektach i znaczeniu zmian; ocenialna odpowiedź i wskazanie źródła w oryginale. |
| oracle | Odpowiedzi ustalone niezależnie od czytnika: diagramy i właściwości w LabVIEW, kontrolowane wejścia/wyjścia, dokumentacja, raporty różnic i zapis niezależnej kontroli. Sam eksport badanego narzędzia nie jest wzorcem. |
| split | Rozdział rozwoju i oceny według całych projektów i rodzin; wykrywanie kopii/wariantów. Nowe własne przypadki ograniczają ryzyko znajomości publicznych przykładów przez model. Klucz i część oceniająca poza dostępem badanego agenta; w publicznym repo nie da się ukryć ich samą ścieżką. Przed pomiarem sprawdzić faktyczną izolację. |
| coverage | Inwentaryzacja wszystkich rodzin, wersji, modułów i warunków dostępu; pokrycie jawne, bez usuwania trudnych przypadków z mianownika. Pierwszy zestaw nie redefiniuje celu. |
| baseline | Powtarzalne porównanie tych samych zadań bez narzędzia, z obrazami gdy dostępne, oraz z narzędziem; ten sam model, prompt i budżet, przypięte wersje, powtórzenia, koszt i czas. |
| challenges | Próby metody na celowo błędnych odpowiedziach, błędnych wskazaniach źródła, stałym/pustym eksporcie i nieobsługiwanym przypadku. Zero wykonanych testów, brak runtime lub klucza nie dają zaliczenia. |

Początkowa inwentaryzacja obejmuje VI (panel i diagram), kontrolki i typedefy, biblioteki,
klasy, projekty i build specs, testy, zasoby, zależności, pakiety, skompilowane dystrybucje
oraz warianty modułów i targetów; lista pozostaje otwarta. Wyniki mają osobne przekroje
według rodziny, wersji zapisu i środowiska. Nieprzebadana wersja ma brak pokrycia.
Wariant 2024 wolno wybrać dopiero po przedstawieniu dodatkowego nakładu dla wszystkich
wersji i ograniczeń zgodności, zgodnie z celem; ten setup nie wybiera wariantu zapasowego.

Przyszły raport oddzieli wierność odczytu od poprawności odpowiedzi agentów i ich poparcia
w źródle. Wskaże liczbę zaplanowanych i rzeczywiście wykonanych przypadków oraz wyniki
poprawne, częściowe, nieobsługiwane, brak zależności/licencji/środowiska, chroniony/usunięty
diagram i błąd narzędzia. Uczciwe zgłoszenie ograniczenia nie dowodzi pełnego odczytu.
Sprawdzenie struktury bez sprzętu nie potwierdza zachowania na sprzęcie. Tolerancje,
niedeterminizm i przedziały niepewności trzeba określić przed porównaniem. Nie agregować
tych wymiarów do arbitralnego jednego wyniku ani nie przyjmować progu sukcesu bez właściciela.

## Niezależna kontrola zmian

Evaluator zmienia tylko uprawniona rola, na zlecenie Policymakera. Silnik wymaga odrębnej
sesji weryfikatora i przypina jej zgodę do commita i drzewa evaluatora. Stara wersja
obowiązuje do wyniku `pass`; zmieniony snapshot wymaga ponownej kontroli.
Instrukcje weryfikatora, wspólny kontrakt roli i protokół są chronione w `engine.yml`.
Silnik blokuje też zmianę/usunięcie wpisu `evaluator-verifier` w profilach, zachowując
możliwość tworzenia pozostałych ról. Zmiana tych zabezpieczeń należy do właściciela.
Niezależność oznacza osobną sesję i dowody, nie gwarancję bezbłędności modelu; przy
niepewności weryfikator odmawia `pass`. To nie bramka końcowego sukcesu (temat D).
