# Cel projektu

Stworzyć narzędzie, które pozwoli agentom AI czytać kod, projekty i wszystkie artefakty LabVIEW tak samo jak zwykły kod.

Priorytetem jest obsługa wszystkich wersji LabVIEW. Jeżeli rozpoznanie wykaże, że wymaga to znacznie większego nakładu czasu niż obsługa jednej wersji, dopuszczonym wariantem zapasowym jest LabVIEW 2024. Przed wyborem wariantu przedstawić oszacowanie różnicy nakładu i ograniczenia zgodności; nie ustalono liczbowego progu „znacznie większego”. Wariant zapasowy dotyczy wersji LabVIEW, a nie ograniczenia rodzajów artefaktów.

Przed implementacją narzędzia opracować wiarygodny benchmark lub inną powtarzalną metodę weryfikacji, która pozwoli sprawdzić, czy narzędzie działa.

## Uzgodnione zasady sukcesu — 18.10.2026

Właściciel zaakceptował następujące zasady:

- Osobno sprawdzać wierność odczytu artefaktów oraz poprawność odpowiedzi agenta i ich poparcie wskazaniem źródła w oryginalnym artefakcie.
- Stosować niezależnie ustalone odpowiedzi wzorcowe, przypadki niewykorzystywane przy budowie rozwiązania oraz powtarzalne porównanie z pracą bez narzędzia. Szczegóły metody określa `docs/perpetua/evaluation.md`.
- Sprawdzać rzeczywiste zadania, np. wyjaśnienie obliczeń VI i zależności wykonania, znalezienie zależności projektu i skutków zmiany typedefu oraz wyjaśnienie znaczenia różnicy między diagramami. Przykłady nie ograniczają zakresu celu.
- Raportować pokrycie według rodzajów artefaktów i wersji. Brak obsługi, zależności, licencji, środowiska lub dostępnego diagramu pozostaje widocznym brakiem; nie jest zaliczeniem pełnego odczytu ani zgodą na wyłączenie przypadku z zakresu.

Pełny cel pozostaje w mocy. Konkretne progi jakości i wykonywalna bramka zakończenia wymagają osobnej akceptacji właściciela po przygotowaniu wiarygodnego benchmarku. Uzgodnienie tych zasad nie potwierdza gotowości benchmarku ani skuteczności produktu i nie zastępuje akceptacji metody przed implementacją.

Przyszła bramka ma wymagać końcowego potwierdzenia właściciela (`owner_confirms: true`). Na tym etapie nie przyjęto komendy bramki i nie tworzy się `goal/gate.yml`; bez zaakceptowanej bramki pętla nie może samodzielnie ogłosić osiągnięcia celu.
