using UnityEngine;
using System.Collections;

public class PlayerController_Warrior : MonoBehaviour {
	//Public
	public float moveSpeed = 5.0f;
	public float projectileSpeed = 10.0f;
	//Spells
	public GameObject Swipe;

	//Private
	private Vector2 target;
	private Vector2 direction;
	
	
//Update
	void Update () {
		Movement();

		if (Input.GetKeyDown (KeyCode.Alpha1)) {
			TargetMouse();
			SpawnPojectile(Swipe,false);
		}
	}
//Targets Mouse
	void TargetMouse(){
		target = Camera.main.ScreenToWorldPoint(Input.mousePosition);
		direction = target - ((Vector2)transform.position);	
		direction.Normalize();
	}
	
//Cast given spell	
	void SpawnPojectile(GameObject spawnThis, bool hasVelocity){
		GameObject projectile = Instantiate(spawnThis, (Vector2)transform.position+(direction/2),Quaternion.identity) as GameObject;
		if(hasVelocity)projectile.rigidbody2D.velocity += direction*projectileSpeed;
			else projectile.transform.position = (Vector2)projectile.transform.position + (direction*1.5f);
		RotateProjectile(projectile);
	}
	
//Rotates Projectile so it looks good
	void RotateProjectile(GameObject projectile){
		/*float angle = Mathf.Atan2(projectile.rigidbody2D.velocity.y,projectile.rigidbody2D.velocity.x) * Mathf.Rad2Deg;*/
		float angle = Mathf.Atan2(direction.y,direction.x) * Mathf.Rad2Deg;
		projectile.transform.rotation = Quaternion.AngleAxis(angle,Vector3.forward);
	}
	
//Player Movement
	private void Movement(){
		
		if(Input.GetKey(KeyCode.W)){
			transform.position += new Vector3(0.0f,moveSpeed*Time.deltaTime,0.0f);
		}
		if(Input.GetKey(KeyCode.S)){
			transform.position += new Vector3(0.0f,-moveSpeed*Time.deltaTime,0.0f);
		}
		if(Input.GetKey(KeyCode.D)){
			transform.position += new Vector3(moveSpeed*Time.deltaTime,0.0f,0.0f);
		}
		if(Input.GetKey(KeyCode.A)){
			transform.position += new Vector3(-moveSpeed*Time.deltaTime,0.0f,0.0f);
		}
	}
	
}
