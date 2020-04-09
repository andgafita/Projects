import java.util.ArrayList;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;

public class LinksFromBoards 
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
		
		driver.get("http://fiistudent.ddns.us/personalise/boards/");
		
		
		for(char elem='1';elem<='7';elem++)
		{
			String xpath="//a[@href='" +elem+ "/']";
			System.out.println(driver.findElement(By.xpath(xpath)).getText());
			driver.findElement(By.xpath(xpath)).click();
			driver.findElement(By.xpath("//a[@class='meniu']")).click();
			Thread.sleep(1000);
		}		
		
		driver.close();
		driver.quit();
	}
}
