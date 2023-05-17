using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SpriteScroller : MonoBehaviour
{
    [SerializeField] Vector2 moveSpeed;

    Vector2 offset;
    Material material;
    
    private void Awake() {
        material = GetComponent<SpriteRenderer>().material;
    }

    void Update()
    {
        Scroll();
    }

    void Scroll(){
        offset = Time.deltaTime * moveSpeed; 
        material.mainTextureOffset += offset;
    }
}
