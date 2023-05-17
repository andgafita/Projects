using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Health : MonoBehaviour
{
    [SerializeField] bool isPlayer;
    [SerializeField] int health = 50;
    [SerializeField] int scoreValue = 50;
    [SerializeField] ParticleSystem hitEffect;
    [SerializeField] bool applyCameraShake = false;
    CameraShake cameraShake;
    AudioPlayer audioPlayer;
    ScoreKeeper scoreKeeper;
    LevelManager levelManager;

    private void Awake() {
        cameraShake = Camera.main.GetComponent<CameraShake>();
        audioPlayer = FindObjectOfType<AudioPlayer>();
        scoreKeeper = FindObjectOfType<ScoreKeeper>();
        levelManager = FindObjectOfType<LevelManager>();
    }

    void TakeDamage(int damage){
        health -= damage;

        if(health <= 0){
            Die();
        }
    }

    void Die(){
        if(!isPlayer){//LayerMask.LayerToName(gameObject.layer) == "Enemy"){
            scoreKeeper.AddToScore(scoreValue);
        } else {
            levelManager.LoadGameOver();
        }
        Destroy(gameObject);
    }

    void OnTriggerEnter2D(Collider2D other) {
        DamageDealer damageDealer = other.GetComponent<DamageDealer>();

        if(damageDealer is not null){
            TakeDamage(damageDealer.GetDamage());
            PlayHitEffect();
            ShakeCamera();
            audioPlayer.PlayTakeDamageClip();
            damageDealer.Hit();
        }
    }

    void PlayHitEffect(){
        if(hitEffect is not null){
            Quaternion instantiateQuaternion = (LayerMask.LayerToName(gameObject.layer) == "Player") ? Quaternion.Euler(90f, 0f, 0f) : Quaternion.Euler(-90f, 0f, 0f);

            ParticleSystem instance = Instantiate(hitEffect, transform.position, instantiateQuaternion);
            Destroy(instance.gameObject, instance.main.duration + instance.main.startLifetime.constantMax);
        }
    }

    void ShakeCamera(){
        if(cameraShake is not null && applyCameraShake){
            cameraShake.Play();
        }
    }

    public int GetHealth(){
        return health;
    }
}
