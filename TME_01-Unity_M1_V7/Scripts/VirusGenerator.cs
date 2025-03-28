using UnityEngine;
using System.Collections;

[DisallowMultipleComponent]
public class VirusGenerator : MonoBehaviour
{
    // Le prefab sera défini dans l'Inspector
    public GameObject virusPrefab;
    public BoxCollider2D backgroundBounds;
    public float reloadTime = 2f;
    public float reloadProgress = 0f;


    void Update()
    {
        reloadProgress += Time.deltaTime;
        if (reloadProgress >= reloadTime)
        {
            createVirus();
            reloadProgress = 0;
        }
    }
    public void popVirus(int amount)
    {
        for (int i = 0; i< amount; i++)
        {
            createVirus();
        }
    }
    public void createVirus()
    {
        // Instanciation d'un nouveau virus
        GameObject newVirus = Instantiate(virusPrefab);
        // Assigner le backgroundBounds au virus
        VirusMove virusMove = newVirus.GetComponent<VirusMove>();
        if (virusMove != null)
        {
            virusMove.backgroundBounds = backgroundBounds;
        }
        else
        {
            Debug.LogError("Le prefab du virus n'a pas de composant VirusMove !");
        }
    }
}
