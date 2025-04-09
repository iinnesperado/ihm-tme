Task 2
On peut vérifier qu'il est bien désactiver en bougeant vite avec la souris et revenir au point de départ doucement et voir si le curseur se retrouve à la même place.

Task 3
En observant les courbes on voit qu'on à de meilleur résultat en ayant un c positif et un r compris entre 0 et 1. Plus le c augmente plus la vitesse du curseur augmente donc sa valeur dépend de la préférence de vitesse de l'utilisateur.

Task 4
En utilisant l'AbsoluteCursor, le minimum qu'on peut atteindre avec la souris est 0 si on clique tout de suite et le maximum est 23000 px/s dans notre cas et on a une vitesse moyenne de 1500 px/s

Task 5
En choisissant k=1 le mouvement semble pus confortable car il est semblable au mouvement habituel et donc moins surprenant pour l'utilisateur. En l'utilisant sur une plus longue durée un gain plus élevée peut être mieux selon la préférence de vitesse du curseur.

Task 6
En utilisant les observations des courbes dessinées pour la tache 3 on choisit 0.9 pour r et 2 pour c selon nos préférences de vitesse.

task 7 
La classe PolyCursor permet de voir les différents curseurs en même temps et donc de les comparer.

Task 8 
CustomCursor est plus confortable car il est rapide et ralentit quand on s'approche de la cible.

Task 9
En observant les résultats stockés dans pilot_result, on voit que CustomCursor est un peu plus performant en terme de rapidité que AbsoluteCursor en moyenne (1285.04 px/s contre 1468.07 px/s)

Task 10
La taille estimé de chaque groupe est de 11 personnes donc 22 personnes au total avec alpha=0.05

Task 11
Les résultats s'améliorent après chaque essai.

Task 12
Les résultats observés peuvent être biaisé car il faut prendre en compte l'apprentissage au fur et à mesure des essai car l'utilisateur s'améliore après chaque essai avec un nouveau curseur.

Task 16
La distribution gaussienne et EMG ont respectivement une log vraisemblance de -108.687 et -75.895.

Task 17
La fonction EMG a donc une vraisemblance plus élevée et semble donc plus adapté à nos données cela s'explique par le fait que EMG est en général plus flexible que la gaussienne. De plus en observant le graphique montrant nos deux fonctions sur les données on voit clairement que EMG est plus adapté dans notre cas. Les meilleurs paramètre pour la gaussienne sont μ=1.05 et σ=0.72, pour EMG on a μ=0.43, σ=0.17 et β=0.62

Task 19
L'article "No More Bricolage" écrit par Casiez et al. en 2011 se penche sur l'utilisation et l'efficacité des différents outils de pointage proposés par les systèmes d'exploitation. Il critique en particulier les fonctions de transfert (Control-Display), comme celles vues dans ce TP. En effet, ces fonctions sont souvent trop simplistes et ne reflètent pas fidèlement le comportement réel des utilisateurs. Comme nous avons pu le constater, il faut prendre en compte l’adaptation progressive des utilisateurs au fil des essais. En comparant avec les fonctions utilisées par Windows, macOS ou Xorg, on remarque qu’elles sont plus complexes et optimisées, contrairement à une fonction CD linéaire. L’article souligne aussi l’importance d’outils de mesure comme libpointing, indispensables pour évaluer précisément les performances. Ce TP, centré sur la recherche expérimentale, nous a permis de découvrir comment construire une méthodologie rigoureuse, ce qui pourra être très utile dans nos futures expérimentations.








