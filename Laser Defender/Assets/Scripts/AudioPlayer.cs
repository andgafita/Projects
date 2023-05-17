using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AudioPlayer : MonoBehaviour
{
    [Header("Shooting")]
    [SerializeField] AudioClip shootingClip;
    [SerializeField] [Range(0f, 1f)] float shootingVolume = 1f;

    [Header("TakeDamage")]
    [SerializeField] AudioClip takeDamageClip;
    [SerializeField] [Range(0f, 1f)] float takeDamageVolume;

    static AudioPlayer instance;

    public AudioPlayer GetInstance(){
        return instance;
    }

    private void Awake() {
        ManageSingleton();
    }

    void ManageSingleton(){
        if(instance is not null) {
            gameObject.SetActive(false);
            Destroy(gameObject);
        } else {
            instance = this;
            DontDestroyOnLoad(gameObject);
        }
    }

    public void PlayShootingClip(){
        PlayClip(shootingClip, shootingVolume);
    }

    public void PlayTakeDamageClip(){
        PlayClip(takeDamageClip, takeDamageVolume);
    }

    private void PlayClip(AudioClip clip, float volume){
        if(clip is not null){
            Vector3 cameraPos = Camera.main.transform.position;
            AudioSource.PlayClipAtPoint(clip, cameraPos, volume);
        }
    }
}
