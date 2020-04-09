using UnityEngine;
using System.Collections;

public class SkullSplit : MonoBehaviour {
	public int damage = 125;

	// Use this for initialization
	void Start () {
		Destroy (gameObject,0.35f);
	}
	
	void OnTriggerEnter2D (Collider2D col) {
		if(col.tag == "Enemy"){
		EnemyController enemy = col.GetComponent<EnemyController>();
		enemy.TakeDamage(damage);
		}
	}
}
