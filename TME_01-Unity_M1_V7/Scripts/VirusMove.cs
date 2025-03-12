using UnityEngine;
using System.Collections;

[DisallowMultipleComponent]
public class VirusMove : MonoBehaviour
{

    public float speed = 2.5f;
    public BoxCollider2D backgroundBounds; // reference au collider du background
    private Vector3 targetPosition;
    void Start()
    {
        transform.position= GetRandomPositionInBounds();
        SetNewRandomTarget();
    }

    // Update is called once per frame
    void Update()
    {
        transform.position = Vector3.MoveTowards(
            transform.position,
            targetPosition,
            speed * Time.deltaTime
        );

        // Quand on arrive proche de la cible, on en choisit une nouvelle
        if (Vector3.Distance(transform.position, targetPosition) < 0.1f)
        {
            SetNewRandomTarget();
        }
    }
    private void SetNewRandomTarget()
    {
        targetPosition = GetRandomPositionInBounds();
    }
    private Vector3 GetRandomPositionInBounds()
    {
        if (backgroundBounds == null)
        {
            Debug.LogError("BackgroundBounds non assigné !");
            return Vector3.zero;
        }

        // Récupère les limites du background
        Bounds bounds = backgroundBounds.bounds;

        float offset = 0.25f;
        
        // Génère une position aléatoire dans le rectangle
        return new Vector3(
            Random.Range(bounds.min.x + offset, bounds.max.x - offset),
            Random.Range(bounds.min.y + offset, bounds.max.y - offset),
            0
        );
    }
}