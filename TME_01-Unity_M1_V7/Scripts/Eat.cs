using UnityEngine;
using System.Collections;

[DisallowMultipleComponent]
public class Eat : MonoBehaviour
{
    // Nous impolémentons la méthode OnTriggerEnter2D car nous utilisons
    // des Collider 2D. Si nous avios utilisé des Collider classiques (3D)
    // il aurait fallu implémenter la méthode OnTriggerEnter. Faites donc
    // attention à implémenter la bonne méthode en fonction du bon type de 
    // Collider utilisé.
    void OnTriggerEnter2D(Collider2D other)
    {
        if (other.gameObject.CompareTag("virus")){
            Destroy (other.gameObject);
        }
    }
}
