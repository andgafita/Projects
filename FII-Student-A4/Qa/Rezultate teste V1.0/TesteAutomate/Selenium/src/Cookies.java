import java.util.Set;

import org.openqa.selenium.By;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

import okhttp3.Cookie;

//driver.get("http://fiistudent.ddns.us/users/login/");
//
//driver.findElement(By.name("username")).sendKeys("teodora.calarasu@students.info.uaic.ro");
//driver.findElement(By.name("password")).sendKeys("valoare1");
//driver.findElement(By.xpath("//input[@type='submit']")).click();
//
//driver.get("http://fiistudent.ddns.us");
//driver.findElement(By.xpath("//a[@href='/orar/']")).click();
//
//String firstXpath="//button[@type='submit']";

public class Cookies 
{
	public static void main(String[] args) throws InterruptedException
	{
		System.setProperty("webdriver.chrome.driver", "C:\\Users\\Tudor\\Desktop\\selenium\\chromedriver.exe");
		WebDriver driver=new ChromeDriver();
		driver.get("http://fiistudent.ddns.us/users/login/");
		
		driver.findElement(By.name("username")).sendKeys("teodora.calarasu@students.info.uaic.ro");
		driver.findElement(By.name("password")).sendKeys("valoare1");
		driver.findElement(By.xpath("//input[@type='submit']")).click();
		Set<org.openqa.selenium.Cookie> set=driver.manage().getCookies();
		Thread.sleep(3000);
		
		System.out.println(set.size());
		for(org.openqa.selenium.Cookie cookie:set)
		{
			System.out.println(cookie.getName());
		}
		
		driver.manage().deleteCookieNamed("sessionid");
		Thread.sleep(3000);
		
		driver.findElement(By.xpath("//a[@href='/news/']")).click();
		Thread.sleep(3000);
		driver.findElement(By.xpath("//a[@href='/orar/']")).click();
		Thread.sleep(3000);
		
		System.out.println(driver.manage().getCookies().size());
		driver.close();
		driver.quit();
	}
}
