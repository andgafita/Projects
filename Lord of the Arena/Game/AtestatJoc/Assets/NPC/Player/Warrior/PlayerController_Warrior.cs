using UnityEngine;
using System.Collections;

public class PlayerController_Warrior : MonoBehaviour {
	//Public
	public float moveSpeed = 5.0f;
	public float projectileSpeed = 10.0f;
	//Stats
	public struct stats{public int defaultHealth, defaultVitality, defaultRage;
		public int Health, Vitality, Rage;
		public int Strength, Endurance, Stamina, Armor;
		//Strength
		public void SetStrength(int setStrength){
			Strength = setStrength;
			Rage = defaultRage + Strength*10;
		}
		public int GetStrength(){return Strength;}
		//Endurance
		public void SetEndurance(int setEndurance){
			Endurance = setEndurance;
			Vitality = defaultVitality + Endurance*10;
		}
		public int GetEndurance(){return Endurance;}
		//Stamina
		public void SetStamina(int setStamina){
			Stamina = setStamina;
			Health = defaultHealth + Stamina*15;
		}
		public int GetStamina(){return Stamina;}
		//Armor
		public void SetArmor(int setArmor){
			Armor = setArmor;
		}
		public int GetArmor(){return Armor;}
		//Set the base stats of health mana and vitality
		public void SetDefaultStats(int health, int rage, int vitality){
			defaultHealth = health;
			defaultRage = rage;
			defaultVitality = vitality;
		}
	}
	public stats Stats;
	//Spells
	public GameObject AutoAttack;
	public GameObject Swipe;
	public GameObject SkullSplit;
	public GameObject ThunderStomp;
	public GameObject ShieldBash;
	public GameObject SoundBlast;
	//Private
	private Vector2 target;
	private Vector2 direction;

	//Start
	void Start(){
		Stats.SetDefaultStats (150,100,50);
		Stats.SetStrength (2);
		Stats.SetStamina (4);
		Stats.SetEndurance (3);
		Stats.SetArmor (2);
		UpdateAttacksDamage ();

	}
//Update
	void Update () {
		Movement();
		CheckForSpells();
	}
	
	
	//Checks for spells
	void CheckForSpells(){
		if(Input.GetKeyDown(KeyCode.Alpha1)){
			TargetMouse();
			SpawnPojectile(AutoAttack,false,1f,1.2f);
		}
		if (Input.GetKeyDown (KeyCode.Alpha2)) {
			TargetMouse();
			SpawnPojectile(Swipe,false,1.2f,1f);
		}
		if(Input.GetKeyDown(KeyCode.Alpha3)){
			TargetMouse();
			SpawnPojectile(SkullSplit,false,1f,1.6f);
		}
		if(Input.GetKeyDown(KeyCode.Alpha4)){
			Instantiate(ThunderStomp,transform.position,Quaternion.identity);
		}
		if(Input.GetKeyDown(KeyCode.Alpha5)){
			TargetMouse();
			SpawnPojectile(ShieldBash,false,1f,1.8f);
		}
		if (Input.GetKeyDown (KeyCode.Alpha6)) {
			TargetMouse();
			SpawnPojectile(SoundBlast,false,1.2f,1f);
		}
	}

	//Updates Attack Damage
	void UpdateAttacksDamage(){
		int AttackPower = Stats.GetStrength () * 10;
		AutoAttack.GetComponent<AutoAttack>().damage = AutoAttack.GetComponent<AutoAttack>().defaultDamage + AttackPower;
		Swipe.GetComponent<Swipe>().damage = Swipe.GetComponent<Swipe>().defaultDamage + AttackPower;
		SkullSplit.GetComponent<SkullSplit>().damage = SkullSplit.GetComponent<SkullSplit>().defaultDamage + AttackPower;
		ThunderStomp.GetComponent<ThunderStomp>().damage = ThunderStomp.GetComponent<ThunderStomp>().defaultDamage + AttackPower;
		ShieldBash.GetComponent<ShieldBash>().damage = ShieldBash.GetComponent<ShieldBash>().defaultDamage + AttackPower;
		SoundBlast.GetComponent<SoundBlast>().damage = SoundBlast.GetComponent<SoundBlast>().defaultDamage + AttackPower;
	}
//Targets Mouse
	void TargetMouse(){
		target = Camera.main.ScreenToWorldPoint(Input.mousePosition);
		direction = target - ((Vector2)transform.position);	
		direction.Normalize();
	}
	
//Cast given spell	
	void SpawnPojectile(GameObject spawnThis, bool hasVelocity,float distanceMultiplier,float distanceDivider){
		GameObject projectile = Instantiate(spawnThis, (Vector2)transform.position+((direction*distanceMultiplier)/distanceDivider),Quaternion.identity) as GameObject;
		if(hasVelocity)projectile.rigidbody2D.velocity += direction*projectileSpeed;
			else projectile.transform.position = (Vector2)projectile.transform.position + ((direction*distanceMultiplier)/distanceDivider);
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
