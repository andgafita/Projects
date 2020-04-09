using UnityEngine;
using System.Collections;

public class FrozenLance : MonoBehaviour {
	public int damage = 30;
	public int FrozenLanceBonusDamage = 70;

	void OnTriggerEnter2D (Collider2D col){
		if (col.tag == "Enemy") {
			EnemyController enemy = col.GetComponent<EnemyController>();
			enemy.TakeDamage(damage);
			if(enemy.isFrozenNow)enemy.TakeDamage(FrozenLanceBonusDamage);
		}
		Destroy (gameObject);
	}

}
