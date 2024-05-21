# Scientific String Parser Development

## Project Overview

### Objective
The primary objective of this internship is to develop a scientific string parser that can split scientific strings into their respective metadata. This parser will replace the discontinued Freecite tool and will be used by the Flanders Marine Institute (VLIZ) to manage and search references in the WoRMS (World Register of Marine Species) database.

### Goals
1. **Create a Local Tool:** Develop a parser that can operate locally on the VLIZ servers.
2. **Match or Exceed Freecite Performance:** Ensure the new tool performs as well or better than Freecite.
3. **Handle Difficult References:** Develop capabilities to handle challenging or incorrectly split references.
4. (**Use Machine Learning:** Integrate machine learning to improve parsing accuracy over time.) (tbd)
5. **Docker Containerization:** Ensure the tool can be containerized with Docker for easy deployment.

### Files
- Scripts: contains python scripts that are used to convert XML GROBID ouput into CSV for analysis in excel
- Server scripts: contains bash scripts that are used to automate API requests on a VLIZ server
