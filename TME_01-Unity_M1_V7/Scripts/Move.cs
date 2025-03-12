using UnityEngine;
using System.Collections;

[DisallowMultipleComponent]
public class Move : MonoBehaviour
{

    public float speed = 2.5f;
    public BoxCollider2D backgroundBounds;
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        Vector3 movement = Vector3.zero;

        if(Input.GetKey(KeyCode.LeftArrow)==true)
            movement += Vector3.left;
        if(Input.GetKey(KeyCode.RightArrow)==true)
            movement += Vector3.right;
        if(Input.GetKey(KeyCode.UpArrow)==true)
            movement += Vector3.up;
        if(Input.GetKey(KeyCode.DownArrow)==true)
            movement += Vector3.down;
        
        Vector3 newPosition = transform.position + movement * speed * Time.deltaTime;

        newPosition = ClampPositionToBackground(newPosition);
        transform.position = newPosition;
    }
    private Vector3 ClampPositionToBackground(Vector3 position)
    {
        if (backgroundBounds == null)
        {
            Debug.LogError("BackgroundBounds non assigné !");
            return position;
        }

        // Récupère les limites du background
        Bounds bounds = backgroundBounds.bounds;

        // Prend en compte la taille du macrophage (si nécessaire)
        float offset = 0.25f; // Ajuste cette valeur selon la taille de ton GameObject

        // Limite la position aux bords du background
        position.x = Mathf.Clamp(position.x, bounds.min.x + offset, bounds.max.x - offset);
        position.y = Mathf.Clamp(position.y, bounds.min.y + offset, bounds.max.y - offset);

        return position;
    }
}
