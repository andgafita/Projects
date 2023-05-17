using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

public class UIDisplay : MonoBehaviour
{
    [Header("Health")]
    [SerializeField] Health healthScript;
    [SerializeField] Slider slider;
    
    [Header("Score")]
    [SerializeField]TextMeshProUGUI scoreText;
    ScoreKeeper scoreKeeper;

    int maxHealth;


    private void Awake() {
        maxHealth = healthScript.GetHealth();
        scoreKeeper = FindObjectOfType<ScoreKeeper>();
    }

    private void Start() {
        slider.maxValue = healthScript.GetHealth();
    }

    private void Update() {
        slider.value = healthScript.GetHealth();
        scoreText.text = scoreKeeper.GetScore().ToString("000000000");
    }
}
