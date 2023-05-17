using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Enemy : MonoBehaviour
{
    [SerializeField] int scorePerHit = 25;
    [SerializeField] int hitPoints = 5;
    [SerializeField] int damagePerHit = 1;
    [SerializeField] GameObject deathVFX;
    [SerializeField] GameObject onHitVFX;

    Rigidbody rb;
    ScoreBoard scoreBoard;
    Transform spawnAtRuntimeParent;
    List<ParticleCollisionEvent> collisionEvents;

    void Start()
    {
        scoreBoard = FindObjectOfType<ScoreBoard>();
        collisionEvents = new List<ParticleCollisionEvent>();

        spawnAtRuntimeParent = GameObject.FindWithTag("SpawnAtRuntime").transform;

        AddRigidBody();
    }

    void AddRigidBody()
    {
        rb = gameObject.AddComponent<Rigidbody>();
        rb.useGravity = false;
    }

    void OnParticleCollision(GameObject other)
    {
        other.GetComponent<ParticleSystem>().GetCollisionEvents(gameObject, collisionEvents);
        ProcessHit();
    }


    void ProcessDeathVFX()
    {
        GameObject vfx = Instantiate(deathVFX, transform.position, Quaternion.identity);
        vfx.transform.parent = spawnAtRuntimeParent;
    }

    void ProcessOnHitVFX(Vector3 hitPosition)
    {
        if(onHitVFX != null){
            GameObject vfx = Instantiate(onHitVFX, hitPosition, Quaternion.identity);
        }
    }

    void Die()
    {
        scoreBoard.increaseScore(scorePerHit);
        ProcessDeathVFX();
        Destroy(gameObject, 0f);
    }

    void dealDamage(){
        hitPoints -= damagePerHit;

        if(hitPoints <= 0){
            Die();
        }
    }

    void ProcessHit()
    {
        foreach(var colEvent in collisionEvents){
            ProcessOnHitVFX(colEvent.intersection);
        }

        dealDamage();
    }
}
