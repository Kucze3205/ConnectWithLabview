# Cel projektu

Stworzyć narzędzie, które pozwoli agentom AI czytać oraz pisać kod, projekty i wszystkie artefakty LabVIEW tak samo jak zwykły kod.

Priorytetem jest obsługa wszystkich wersji LabVIEW. Jeżeli rozpoznanie wykaże, że wymaga to znacznie większego nakładu czasu niż obsługa jednej wersji, dopuszczonym wariantem zapasowym jest LabVIEW 2024. Przed wyborem wariantu przedstawić oszacowanie różnicy nakładu i ograniczenia zgodności; nie ustalono liczbowego progu „znacznie większego”. Wariant zapasowy dotyczy wersji LabVIEW, a nie ograniczenia rodzajów artefaktów.

Przed implementacją narzędzia opracować wiarygodny benchmark lub inną powtarzalną metodę weryfikacji, która pozwoli sprawdzić, czy narzędzie działa.

## Pisanie

Pisanie obejmuje tworzenie i zmienianie artefaktów tak samo jak w zwykłym kodzie: agent czyta, zmienia, sprawdza wynik i uczciwie raportuje. Sposób zapisu wybiera pętla i uzasadnia ten wybór. Edycja nie wymaga LabVIEW; sprawdzenie (kompilacja i uruchomienie) może go wymagać, tak jak zwykły kod wymaga interpretera lub kompilatora. Artefakty skompilowane zmienia się przez źródła i przebudowę. Zmieniony plik zachowuje swoją wersję zapisu; zmiana wersji jest widocznym brakiem. Oszacowanie przed wyborem wariantu zapasowego obejmuje też pisanie.

Pisanie rozszerza istniejący benchmark i dane pętli, zamiast budować je od nowa. Implementacja odczytu może ruszyć przed pisaniem; implementacja pisania czeka na akceptację metody obejmującej zadania zapisu.

## Proof of concept

Przed dalszym przygotowaniem benchmarku pętla dostarcza POC, który ma pokazać, że koncepcja ma sens i że gotowy produkt może powstać. Agent, który nie widział wcześniej danego VI, poprawnie opisuje jego diagram i zmienia jego logikę bez użycia LabVIEW. Wynik otwiera się w LabVIEW bez złamanej strzałki, zachowuje się zgodnie z poleceniem i zachowuje wersję zapisu. Prace nad benchmarkiem niepotrzebne do POC czekają do jego dostarczenia.

POC jest wyjątkiem od zasady „najpierw metoda, potem implementacja”. Nie jest produktem ani dowodem jakości; jego kod może trafić do produktu dopiero normalną drogą z testami i przeglądem. Pętla dostarcza pliki, raport i krótką instrukcję, według której właściciel sprawdza wynik ręcznie w swoim LabVIEW. Jeśli POC się nie uda, raport pokazuje dowody i możliwe drogi wyjścia, a pętla nie zmienia celu sama. Pętla nie czeka na odpowiedź właściciela: po dostarczeniu wraca do pracy, a brak odpowiedzi nie jest akceptacją metody, jakości ani produktu.

## Uzgodnione zasady sukcesu — 18.10.2026

Właściciel zaakceptował następujące zasady:

- Osobno sprawdzać wierność odczytu artefaktów oraz poprawność odpowiedzi agenta i ich poparcie wskazaniem źródła w oryginalnym artefakcie.
- Stosować niezależnie ustalone odpowiedzi wzorcowe, przypadki niewykorzystywane przy budowie rozwiązania oraz powtarzalne porównanie z pracą bez narzędzia. Szczegóły metody określa `docs/perpetua/evaluation.md`.
- Sprawdzać rzeczywiste zadania, np. wyjaśnienie obliczeń VI i zależności wykonania, znalezienie zależności projektu i skutków zmiany typedefu oraz wyjaśnienie znaczenia różnicy między diagramami. Przykłady nie ograniczają zakresu celu.
- Raportować pokrycie według rodzajów artefaktów i wersji. Brak obsługi, zależności, licencji, środowiska lub dostępnego diagramu pozostaje widocznym brakiem; nie jest zaliczeniem pełnego odczytu ani zgodą na wyłączenie przypadku z zakresu.

Pełny cel pozostaje w mocy. Konkretne progi jakości i wykonywalna bramka zakończenia wymagają osobnej akceptacji właściciela po przygotowaniu wiarygodnego benchmarku. Uzgodnienie tych zasad nie potwierdza gotowości benchmarku ani skuteczności produktu i nie zastępuje akceptacji metody przed implementacją.

Przyszła bramka ma wymagać końcowego potwierdzenia właściciela (`owner_confirms: true`). Na tym etapie nie przyjęto komendy bramki i nie tworzy się `goal/gate.yml`; bez zaakceptowanej bramki pętla nie może samodzielnie ogłosić osiągnięcia celu.
