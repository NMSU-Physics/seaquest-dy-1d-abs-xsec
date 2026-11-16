#!/usr/bin/env python3
import os

tex_content = r"""\documentclass{beamer}
\usetheme{Madrid}
\usecolortheme{default}
\usepackage{graphicx}
\usepackage{booktabs}

\title[E906 Beam Diagnostics]{E906 (SeaQuest) Beam Monitor Stability Analysis}
\subtitle{Roadset Comparison and Ratio Diagnostics}
\author{Chatura Kuruppu}
\date{\today}

\begin{document}

% 1. Title Slide
\begin{frame}
  \titlepage
\end{frame}

% 2. Outline
\begin{frame}{Introduction \& Outline}
  \begin{itemize}
    \item \textbf{Objective}: Evaluate beam monitor stability across E906 Roadsets (RS 57, 59, 62, 67, 70).
    \item \textbf{Methodology}: Normalizing the local target monitor (\texttt{E906BM}) against upstream reference monitors (\texttt{G2SEM}, \texttt{NM3SEM}, \texttt{NM3ION}) to check accelerator spill fluctuations.
    \item \textbf{Presentation Flow}:
      \begin{itemize}
        \item Run 2 Dataset (RS 57 \& 59 with Ion Chambers).
        \item Run 3 Dataset (RS 62, 67 \& 70 with Secondary Emission Monitors).
      \end{itemize}
  \end{itemize}
\end{frame}

% 3. RS 57 & 59 - G2SEM
\begin{frame}{RS 57 \& 59: Upstream Reference Monitor (\texttt{G2SEM})}
  \begin{figure}
    \centering
    \includegraphics[width=0.85\textwidth,height=0.7\textheight,keepaspectratio]{result/gr_e906bm_g2sem_rs57_59.pdf}
    \caption{E906BM / G2SEM ratio across Spill IDs for RS 57 and RS 59.}
  \end{figure}
\end{frame}

% 4. RS 57 & 59 - NM3ION
\begin{frame}{RS 57 \& 59: Target Ion Chamber (\texttt{NM3ION})}
  \begin{figure}
    \centering
    \includegraphics[width=0.85\textwidth,height=0.7\textheight,keepaspectratio]{result/gr_e906bm_nm3ion_rs57_59.pdf}
    \caption{E906BM / NM3ION ratio across Spill IDs for RS 57 and RS 59.}
  \end{figure}
\end{frame}

% 5. RS 57 & 59 - Overlaid
\begin{frame}{RS 57 \& 59: Overlaid Ratios Comparison}
  \begin{figure}
    \centering
    \includegraphics[width=0.85\textwidth,height=0.7\textheight,keepaspectratio]{result/gr_e906bm_g2sem_and_nm3ion_overlaid_rs57_59.pdf}
    \caption{Combined overlaid view of G2SEM and NM3ION normalizations for RS 57 \& 59.}
  \end{figure}
\end{frame}

% 6. RS 57 & 59 - Two-Pad
\begin{frame}{RS 57 \& 59: Two-Pad Split Comparison}
  \begin{figure}
    \centering
    \includegraphics[width=0.85\textwidth,height=0.7\textheight,keepaspectratio]{result/gr_e906bm_g2sem_and_nm3ion_2pads_rs57_59.pdf}
    \caption{Side-by-side two-pad canvas layout for RS 57 \& 59.}
  \end{figure}
\end{frame}

% 7. RS 62, 67 & 70 - G2SEM
\begin{frame}{RS 62, 67 \& 70: Upstream Reference Monitor (\texttt{G2SEM})}
  \begin{figure}
    \centering
    \includegraphics[width=0.85\textwidth,height=0.7\textheight,keepaspectratio]{result/gr_e906bm_g2sem_rs62_67_70.pdf}
    \caption{E906BM / G2SEM ratio across Spill IDs for RS 62, 67, and 70.}
  \end{figure}
\end{frame}

% 8. RS 62, 67 & 70 - NM3SEM
\begin{frame}{RS 62, 67 \& 70: Secondary Emission Monitor (\texttt{NM3SEM})}
  \begin{figure}
    \centering
    \includegraphics[width=0.85\textwidth,height=0.7\textheight,keepaspectratio]{result/gr_e906bm_nm3sem_rs62_67_70.pdf}
    \caption{E906BM / NM3SEM ratio across Spill IDs for RS 62, 67, and 70.}
  \end{figure}
\end{frame}

% 9. RS 62, 67 & 70 - Overlaid
\begin{frame}{RS 62, 67 \& 70: Overlaid Ratios Comparison}
  \begin{figure}
    \centering
    \includegraphics[width=0.85\textwidth,height=0.7\textheight,keepaspectratio]{result/gr_e906bm_g2sem_and_nm3sem_overlaid_rs62_67_70.pdf}
    \caption{Combined overlaid view of G2SEM and NM3SEM normalizations for RS 62, 67, 70.}
  \end{figure}
\end{frame}

% 10. RS 62, 67 & 70 - Two-Pad
\begin{frame}{RS 62, 67 \& 70: Two-Pad Split Comparison}
  \begin{figure}
    \centering
    \includegraphics[width=0.85\textwidth,height=0.7\textheight,keepaspectratio]{result/gr_e906bm_g2sem_and_nm3sem_2pads_rs62_67_70.pdf}
    \caption{Side-by-side two-pad canvas layout for RS 62, 67, and 70.}
  \end{figure}
\end{frame}

 %% 11. Summary
 %\begin{frame}{Summary \& Conclusions}
 %  \begin{itemize}
 %    \item \textbf{Beam Stability}: Ratio bands remain stable horizontally across spills, confirming consistent beam transport and detector linearity.
 %    \item \textbf{Calibration Shifts}: Distinct step changes between Roadsets highlight detector high-voltage adjustments or steering differences.
 %    \item \textbf{Automation}: The PyROOT + LaTeX Beamer pipeline successfully packages all diagnostic plots into a clean, reproducible slide deck.
 %  \end{itemize}
 %\end{frame}

% 12. End Slide
\begin{frame}
  \centering
  \Huge Thank You!
\end{frame}

\end{document}
"""

with open("presentation.tex", "w") as f:
    f.write(tex_content)

print("Successfully generated presentation.tex!")