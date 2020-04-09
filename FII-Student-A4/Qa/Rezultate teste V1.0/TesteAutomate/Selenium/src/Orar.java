
import java.awt.List;
import java.sql.Driver;
import java.util.ArrayList;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.Select;



public class Orar 
{
	public static void main(String[] args) throws InterruptedException
	{
		
		System.setProperty("webdriver.chrome.driver", "C:\\Users\\Tudor\\Desktop\\selenium\\chromedriver.exe");
		WebDriver driver=new ChromeDriver();
		driver.get("http://fiistudent.ddns.us/users/login/");
		
		driver.findElement(By.name("username")).sendKeys("teodora.calarasu@students.info.uaic.ro");
		driver.findElement(By.name("password")).sendKeys("valoare1");
		driver.findElement(By.xpath("//input[@type='submit']")).click();
		
		driver.get("http://fiistudent.ddns.us");
		driver.findElement(By.xpath("//a[@href='/orar/']")).click();
		
		String firstXpath="//button[@type='submit']";
		
		java.util.List<WebElement> lista=new ArrayList<>();
		lista=driver.findElements(By.xpath(firstXpath));
		System.out.println(lista.get(0));
		
		
		for(int i=1;i<=30;i++)
		{
			Select category=new Select(driver.findElement(By.name("materie")));
			category.selectByIndex(i);
			for(int j=1;j<=20;j++)
			{
				Select category2=new Select(driver.findElement(By.name("grupa")));
				category2.selectByIndex(j);
				for(int k=1;k<=30;k++)
				{
					Select category3=new Select(driver.findElement(By.name("profesor")));
					category3.selectByIndex(k);
					for(int d=1;d<=18;d++)
					{
						Select category4=new Select(driver.findElement(By.name("sala")));
						category4.selectByIndex(d);
					}
				}
			}
		}
		
		
		driver.close();
		driver.quit();
		
	}
}
