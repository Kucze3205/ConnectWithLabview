# Plan początkowy (initial approach)

Wersja robocza z 20 października 2026, do przeglądu przez właściciela przed uzbrojeniem pętli.
Opisuje, jak pętla może dojść do [celu](../../goal/goal.md), i z czego wynikają wymagania wobec środowiska.
Plan jest rewidowalny: pętla poprawia go w miarę uczenia się; zmiana celu lub zakresu wymaga akceptacji
właściciela. Powstał retrospektywnie z już zaakceptowanych ustaleń (nie dodaje żadnych nowych wymagań):
[ocena](evaluation.md), [środowisko](environment.md), [role](roles.md), [granice](accepted-limits.md),
[parametry](operating-parameters.md), [wybór modeli](model-selection.md).

## Kroki

| # | Krok | Zależy od | Potrzebne źródła, narzędzia i dostęp | Weryfikacja |
|---|---|---|---|---|
| 1 | Rozpoznanie: rodzaje artefaktów LabVIEW, wersje, drogi odczytu, formy dostarczenia (MCP jest tylko jedną z opcji) oraz oszacowanie nakładu „wszystkie wersje” kontra LabVIEW 2024 | — | publiczne przykłady i parsery przygotowane przez `prepare.sh`; dokumentacja NI; role bez internetu pracują na przygotowanych źródłach | wnioski w `docs/research/` ze wskazaniem źródeł; oszacowanie i ograniczenia zgodności przedstawione właścicielowi **przed** wyborem wariantu zapasowego |
| 2 | Przygotowanie benchmarku lub innej powtarzalnej metody: protokół, zadania z życia (wyjaśnienie obliczeń VI, zależności projektu, skutki zmiany typedefu, różnica między diagramami), niezależne odpowiedzi wzorcowe, podział na przypadki rozwojowe i wstrzymane, mapa pokrycia wg rodzajów artefaktów i wersji, porównanie z pracą bez narzędzia, przypadki trudne | 1 | przykłady z kroku 1, natywne przetwarzanie w kontenerze NI 2026 Q1 (zadania zaufane, nie role), rola `benchmark` | indeks `benchmark/preparation.json` z hashami; osobno wierność odczytu i poprawność odpowiedzi z odnośnikiem do oryginału |
| 3 | Niezależny przegląd metody i akceptacja przez właściciela; wtedy progi jakości i wykonywalna bramka celu (`owner_confirms: true`) | 2 | rola `reviewer` na przypiętych drzewach; weryfikator evaluatora dla zmian pomiaru | decyzja właściciela przez bramkę zmian; bez niej implementacja produktu nie rusza |
| 4 | Implementacja narzędzia | 3 | rola `implementation` (zapis tylko do `src/`, `tests/`, `docs/product/` itd.), wynik kroku 1 o formie dostarczenia | testy narzędzia oraz pomiar wg zaakceptowanej metody; niezależny przegląd |
| 5 | Pomiar, raport pokrycia i iteracje poprawek | 4 | evaluator i audyt zlecane przez Policymakera | raport wg rodzaju artefaktu i wersji; braki (licencja, zależność, brak diagramu) widoczne jako braki, nie zaliczone |

Kroki 1 i 2 mogą się częściowo nakładać (benchmark potrzebuje przykładów z rozpoznania), ale nic z kroków 4–5 nie
startuje przed akceptacją z kroku 3.

## Pokrycie wymagań przez środowisko

| Wymaganie | Stan |
|---|---|
| Wykonanie wyłącznie w chmurze (GitHub Actions, Ubuntu); komputer właściciela nie jest runnerem | spełnione, [środowisko](environment.md) |
| Publiczne przykłady i parsery (NI Actor Framework, pylavi) w przypiętych wersjach | spełnione przez `prepare.sh`, poza gitem |
| Natywne przetwarzanie VI (kontener NI 2026 Q1 z przypiętym digestem, bez aktywacji, logowania i sieci) | sprawdzone na przykładzie VI z LV2014; nie dowodzi poprawności czytnika, VI Scripting ani wersji 2024 |
| Dostęp do modeli Claude, Codex i Copilot na subskrypcjach, z przełączaniem po wyczerpaniu limitu i wznowieniem | wdrożone i sprawdzone; pozytywne zadanie Claude odroczone przez właściciela, [uwierzytelnianie](cloud-authentication.md) |
| Wybór modeli według jakości względem zużycia limitów | decyzja właściciela z 20.10.2026, decyduje Policymaker, [wybór modeli](model-selection.md) |
| Role: badanie, benchmark, implementacja, przegląd, evaluator, weryfikator, audyt | skonfigurowane, [role](roles.md) |
| Niezależna ocena i bramka właściciela | `gate.kind: owner`, `check` sprawdza integralność dowodów; skuteczność niezmierzona |

## Znane luki i niewiadome

- Natywne uruchomienie LabVIEW 2024 i zgodność między wersjami są niezweryfikowane.
- Izolacja wstrzymanych przypadków oceny i bezpośrednie natywne uruchamianie LabVIEW z ról nie są zapewnione
  (nie są też deklarowane).
- Nie wskazano prywatnych materiałów ani magazynu oceny; prywatny dostęp wymaga konkretnej zgody właściciela.
- Gotowość benchmarku jest nieudowodniona; żadna liczba jakości nie jest przyjęta.
- Zużycie limitów per model nie jest dziś zapisywane; pętla ma je mierzyć (audyt), żeby Policymaker mógł dobierać modele.
