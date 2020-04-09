using UnityEngine;
using System.Collections;

public class PlayerController_Mage : MonoBehaviour {
	//Public
	public float moveSpeed = 5.0f;
	public float projectileSpeed = 10.0f;
	//Spells
	public GameObject FireBolt;
	public GameObject IceBolt;
	public GameObject FireBall;
	public GameObject FireBlast;
	public GameObject Incinerate;
	public GameObject IceWave;
	public GameObject FrozenLance;
	public GameObject FrostBite;
	//Private
	private Vector2 target;
	private Vector2 direction;
	
	
//Update
	void Update () {
		Movement();
		if(Input.GetKeyDown (KeyCode.Alpha1)){
			TargetMouse();
			SpawnPojectile(FireBolt,true);
		}
		if(Input.GetKeyDown (KeyCode.Alpha2)){
			TargetMouse();
			SpawnPojectile(IceBolt,true);
		}
		if(Input.GetKeyDown (KeyCode.Alpha3)){
			TargetMouse();
			SpawnPojectile(FireBall,true);
		}
		if(Input.GetKeyDown(KeyCode.Alpha4)){
			TargetMouse();
			SpawnPojectile(FireBlast,false);
		}
		if (Input.GetKeyDown (KeyCode.Alpha5)) {
			Instantiate(Incinerate,transform.position,Quaternion.identity);
		}
		if (Input.GetKeyDown (KeyCode.Alpha6)) {
			Instantiate(IceWave,transform.position,Quaternion.identity);
		}
		if (Input.GetKeyDown (KeyCode.Alpha7)) {
			TargetMouse();
			SpawnPojectile(FrozenLance,true);
		}
		if (Input.GetKeyDown (KeyCode.Alpha8)) {
			Instantiate(FrostBite,Camera.main.ScreenToWorldPoint(Input.mousePosition),Quaternion.identity);
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
