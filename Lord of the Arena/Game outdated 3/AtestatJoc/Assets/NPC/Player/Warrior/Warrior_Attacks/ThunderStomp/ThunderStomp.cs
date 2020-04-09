using UnityEngine;
using System.Collections;

public class ThunderStomp : MonoBehaviour {
	public int damage = 15;
	// Use this for initialization
	
	void Start () {
		Destroy(gameObject,0.25f);
	}
	
	// Trigger collide
	void OnTriggerEnter2D (Collider2D col) {
		if(col.tag == "Enemy"){
		EnemyController enemy = col.GetComponent<EnemyController>();
		enemy.TakeDamage(damage);
		//TO DO add slow effect
		}
	}
}
