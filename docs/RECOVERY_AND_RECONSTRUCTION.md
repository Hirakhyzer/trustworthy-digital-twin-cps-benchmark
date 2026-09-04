# Recovery and Reconstruction

The generic recovery loop is:

`DETECT -> DIAGNOSE -> ISOLATE -> RECONSTRUCT -> DEGRADE/RECONFIGURE -> VERIFY -> RECOVER`

The baseline state reconstructor blends telemetry and the twin according to source and twin trust. Real deployments would require domain-specific safety constraints and independent validation.

Recovery evaluation should report reconstruction error, service preservation and time to return to trusted operation separately from detection accuracy.
