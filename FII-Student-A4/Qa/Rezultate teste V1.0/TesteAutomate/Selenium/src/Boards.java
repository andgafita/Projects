import java.util.ArrayList;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;


public class Boards 
{
	public static String[] vector=new String[101];
	public static int dim=-1;
	public static void main(String[] args) throws InterruptedException
	{
		System.setProperty("webdriver.chrome.driver", "C:\\Users\\Tudor\\Desktop\\selenium\\chromedriver.exe");
		WebDriver driver=new ChromeDriver();
		driver.get("http://fiistudent.ddns.us/users/login/");
		
		driver.findElement(By.name("username")).sendKeys("teodora.calarasu@students.info.uaic.ro");
		driver.findElement(By.name("password")).sendKeys("valoare1");
		driver.findElement(By.xpath("//input[@type='submit']")).click();
		
		driver.get("http://fiistudent.ddns.us");
		driver.findElement(By.xpath("//a[@href='/personalise/boards/']")).click();
		
		
		java.util.List<WebElement> list=new ArrayList<>();
		list=driver.findElements(By.xpath("//div[@class='filtru']/button"));
		for(WebElement obj:list)
		{
			
			obj.click();
			Thread.sleep(1000);
			java.util.List<WebElement> list2=new ArrayList<>();
			list2=driver.findElements(By.xpath("//button[@class='btn']"));
			for(WebElement obj2:list2)
			{
				obj2.click();
				Thread.sleep(1000);
			}
		}
		
		driver.close();
		driver.quit();
	}
}
