using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class ScoreBoard : MonoBehaviour
{
    TextMeshProUGUI scoreText;
    int score;

    void Awake() {
        scoreText = GetComponent<TextMeshProUGUI>();
        scoreText.text = "0";
    }


    public void increaseScore(int amountToIncrease){
        score += amountToIncrease;

        scoreText.text = score.ToString();
    }
}
