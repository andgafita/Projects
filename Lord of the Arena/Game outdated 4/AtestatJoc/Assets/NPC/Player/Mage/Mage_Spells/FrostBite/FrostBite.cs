using UnityEngine;
using System.Collections;

public class FrostBite : MonoBehaviour {
	public int defaultDamage = 100;
	public int damage = 100;

	void Start(){
		Destroy (gameObject, 0.0001f);
	}


	void OnTriggerEnter2D(Collider2D col){
		Debug.Log ("carnat");
		if (col.tag == "Enemy") {
			EnemyController enemy = col.GetComponent<EnemyController>();
			if(enemy.isFrozenNow)enemy.TakeDamage(damage);
			else enemy.isFrozen = true;
		}
	}
}
