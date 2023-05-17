using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class CollisionHandler : MonoBehaviour
{
    [SerializeField] float loadDelay = 1f;
    [SerializeField] ParticleSystem explosionEffect;

    void OnTriggerEnter(Collider other) {
        gameOver();
    }

    void gameOver(){
        explosionEffect.Play();
        GetComponent<MeshRenderer>().enabled = false;
        GetComponent<BoxCollider>().enabled = false;

        disablePlayerControls();

        Invoke("restartLevel", loadDelay);
    }

    void restartLevel(){
        int currentSceneIndex = SceneManager.GetActiveScene().buildIndex;

        SceneManager.LoadScene(currentSceneIndex);
    }

    void disablePlayerControls(){
        PlayerController playerControlsComponent = GetComponent<PlayerController>();

        playerControlsComponent.enabled = false;
    }
}
