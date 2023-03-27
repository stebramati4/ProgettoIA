# ProgettoIA
Progetto su algoritmica su grafi per soluzione di problemi con la ricerca

Un labirinto di NXN caselle contiene un mago e un invurgus, un mostro invisibile che si nutre di barbe di mago. 
Alcune celle sono dei pozzi senza fondo da cui l’invurgus non può passare, mentre il mago può sorpassare volando. Altre contengono delle colate di lava che bloccano il passaggio sia al mago che all’invurgus. 
Per volare il mago deve raccogliere un particolare fungo che cresce in alcune celle del labirinto. Ogni fungo gli permetterà di volare due volte. 
Ci sono due uscite nella parte nord del labirinto e il mago parte da una posizione a sud. 
Il mago, per fuggire e preservare la sua barba, utilizza un incantesimo che gli permette di scegliere ad ogni passo la prossima mossa migliore.

L’invurgus ad ogni passo si muoverà scegliendo la posizione adiacente migliore per diminuire la distanza dal mago |x(mago)-x(invurgus)| +|y(mago)-y(invurgus)|, o la successiva in senso antiorario. L’incantesimo conosce la posizione dei funghi, delle uscite, e del invurgus anche se invisibile. L’incantesimo viene lanciato una sola volta.
