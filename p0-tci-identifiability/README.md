# TCI consequence-identifiability preflight

This is a bounded measurement gate. It does not implement TCI, train a BC-RNN, or claim policy performance. `tci_identifiability_smoke.py` uses the qualified robosuite wrapper snapshot path and a deterministic state-only scripted controller solely to test whether real cloned-state action interventions produce an identifiable temporal consequence signal. All branches run in fresh subprocesses. The deterministic controller is a scope limitation: a real BC-RNN checkpoint was not available and must be tested before any scientific pilot.
