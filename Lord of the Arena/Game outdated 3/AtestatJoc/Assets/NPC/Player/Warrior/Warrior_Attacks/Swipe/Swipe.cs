using UnityEngine;
using System.Collections;

public class Swipe : MonoBehaviour {
	public int damage = 75;

	void Start(){
		Destroy (gameObject, 0.5f);
	}

	void OnTriggerEnter2D(Collider2D col){
		if (col.tag == "Enemy") {
			EnemyController enemy = col.GetComponent<EnemyController>();
			enemy.TakeDamage(damage);
		}

	}
}
