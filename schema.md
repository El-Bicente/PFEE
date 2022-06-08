```mermaid
graph LR

    S[("Simplicial valué (.csv)")]:::data
    S --> PAR
    S -- "ajout des faces" --> VTP
    
    PAR[["parser (c++)"]]
    PAR --> R
    PAR --> M
    
    subgraph "Revaluation (c++)"
        R[Calcul du champ de gradient]   
    end
    R -- "ajout du champ de gradient n°1" --> VTP
    
    subgraph "Higra (c++)"
        M["Calcul de la MSF"]
    end
    M -- "ajout du champ de gradient n°2" --> VTP
    
    subgraph "VTK (c++)"
        VTP["Création des fichiers .vtp"]
    end
    VTP --> SC
    
    subgraph "Paraview"
        SC{{"Script Python pour <br /> configurer la scène"}}
        VIS(("Affichage des deux <br /> champs de gradient"))
        SC --> VIS
    end
    
    classDef data fill:#3498DB,stroke:BLACK,stroke-width:2px 

```