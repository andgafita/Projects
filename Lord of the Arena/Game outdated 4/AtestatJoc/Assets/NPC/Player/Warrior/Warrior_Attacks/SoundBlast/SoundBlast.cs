using UnityEngine;
using System.Collections;

public class SoundBlast : MonoBehaviour {
	public int defaultDamage = 30;
	public int damage = 30;

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
