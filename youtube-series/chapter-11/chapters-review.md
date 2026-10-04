# Caption-derived chapters

September 22, 2026. Video: https://www.youtube.com/watch?v=Jiqc8jW1skM
Live duration: 22:05. Downloaded owned English ASR captions via YouTube API.

Compared captions.en.srt against script.md sections A–E. The recording spends
longer on shape tracing and parameter updates than the estimated script, so
chapters use actual caption transitions. ASR spellings such as exor and 10H
are corrected to XOR and Tanh in the chapter labels.

Major anchors: 00:21 Linear; 01:08 constructor; 02:07 random weights;
03:54 Tanh transition; 04:38 MLP; 06:39 shape walkthrough; 09:44 why parameters
must be exposed; 11:59 combine the two lists; 12:52 gradient_step; 14:46 mutable
data access; 15:58 XOR setup; 17:02 initial loss/training loop; 18:10 prediction
comparison; 20:02 final compile and result; 21:02 recap. Boundaries round down
to the relevant whole second. No chapter exceeds five minutes; all are at
least ten seconds, including the final chapter. Labels satisfy 28 characters
and five words maximum.

Keyword audit uses the existing keyword-research.md: Linear, Tanh, MLP, tensor
shapes, parameters, weights and XOR describe visible work. No new performance
or search-volume claims. Preserve the existing description outside chapters.
