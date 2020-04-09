using UnityEngine;
using System.Collections;

public class AutoAttack : MonoBehaviour {
	public int defaultDamage = 25;
	public int damage = 25;
	public float attackspeed=0.15f;

	void Start(){
		Destroy (gameObject, attackspeed);
	}

	void OnTriggerEnter2D(Collider2D col){
		if (col.tag == "Enemy") {
			EnemyController enemy = col.GetComponent<EnemyController>();
			enemy.TakeDamage(damage);
		}

	}
}
