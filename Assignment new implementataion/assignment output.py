Python 3.14.3 (tags/v3.14.3:323c59a, Feb  3 2026, 16:04:56) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.

= RESTART: C:/Users/panee/AppData/Local/Programs/Python/Python314/assignment .py

Loading embedding model...
First run may take some time.

Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.

Loading weights:   0%|          | 0/103 [00:00<?, ?it/s]
Loading weights: 100%|██████████| 103/103 [00:00<00:00, 686.45it/s]
======================================================================
             INDUSTROSENSE AI
======================================================================

Responsible Multimodal Industrial Equipment Diagnostics

Knowledge Base:
 - DOC-01 Equipment Manual
 - DOC-02 SOP Bearing Inspection
 - DOC-03 Incident Log Pump Vibration
 - DOC-04 SOP Emergency Shutdown
 - DOC-05 Maintenance Manual Lubrication Schedule

Creating document chunks...
Number of chunks: 5

Building FAISS vector index...
FAISS index created successfully.


======================================================================
Enter your industrial question (or type 'exit'): Why is the motor overheating?

Agent Route: rag

======================================================================
RETRIEVED EVIDENCE - TOP 3
======================================================================

1. DOC-01 Equipment Manual
Similarity Score: 0.5849
Evidence: Motor temperature should remain within the rated operating range. Inspect cooling and ventilation when temperature rises. Check whether the cooling fan is operating correctly. Ensure ventilation openings are not blocked.

2. DOC-02 SOP Bearing Inspection
Similarity Score: 0.3105
Evidence: Inspect abnormal noise, vibration, lubrication problems, and visible wear when checking bearings. Bearing condition should be checked during scheduled maintenance.

3. DOC-03 Incident Log Pump Vibration
Similarity Score: 0.2682
Evidence: Previous pump vibration incidents were associated with bearing wear and shaft misalignment. Check bearing condition and alignment when unusual vibration occurs.


======================================================================
GROUNDED AI RESPONSE
======================================================================
Based on the retrieved industrial documents:

[DOC-01 Equipment Manual] Motor temperature should remain within the rated operating range. Inspect cooling and ventilation when temperature rises. Check whether the cooling fan is operating correctly. Ensure ventilation openings are not blocked.

[DOC-02 SOP Bearing Inspection] Inspect abnormal noise, vibration, lubrication problems, and visible wear when checking bearings. Bearing condition should be checked during scheduled maintenance.

[DOC-03 Incident Log Pump Vibration] Previous pump vibration incidents were associated with bearing wear and shaft misalignment. Check bearing condition and alignment when unusual vibration occurs.


Recommended approach: inspect the relevant equipment condition and follow the applicable manufacturer manual or SOP.


This is an advisory AI response and should not replace qualified human verification.


SAFETY STATUS:
Normal safety check passed.

✓ Basic safety check passed.


======================================================================
Enter your industrial question (or type 'exit'): What could cause pump vibration?

Agent Route: rag

======================================================================
RETRIEVED EVIDENCE - TOP 3
======================================================================

1. DOC-03 Incident Log Pump Vibration
Similarity Score: 0.6543
Evidence: Previous pump vibration incidents were associated with bearing wear and shaft misalignment. Check bearing condition and alignment when unusual vibration occurs.

2. DOC-02 SOP Bearing Inspection
Similarity Score: 0.3835
Evidence: Inspect abnormal noise, vibration, lubrication problems, and visible wear when checking bearings. Bearing condition should be checked during scheduled maintenance.

3. DOC-01 Equipment Manual
Similarity Score: 0.3191
Evidence: Motor temperature should remain within the rated operating range. Inspect cooling and ventilation when temperature rises. Check whether the cooling fan is operating correctly. Ensure ventilation openings are not blocked.


======================================================================
GROUNDED AI RESPONSE
======================================================================
Based on the retrieved industrial documents:

[DOC-03 Incident Log Pump Vibration] Previous pump vibration incidents were associated with bearing wear and shaft misalignment. Check bearing condition and alignment when unusual vibration occurs.

[DOC-02 SOP Bearing Inspection] Inspect abnormal noise, vibration, lubrication problems, and visible wear when checking bearings. Bearing condition should be checked during scheduled maintenance.

[DOC-01 Equipment Manual] Motor temperature should remain within the rated operating range. Inspect cooling and ventilation when temperature rises. Check whether the cooling fan is operating correctly. Ensure ventilation openings are not blocked.


Recommended approach: inspect the relevant equipment condition and follow the applicable manufacturer manual or SOP.


This is an advisory AI response and should not replace qualified human verification.


SAFETY STATUS:
Normal safety check passed.

✓ Basic safety check passed.


======================================================================
Enter your industrial question (or type 'exit'): exit
