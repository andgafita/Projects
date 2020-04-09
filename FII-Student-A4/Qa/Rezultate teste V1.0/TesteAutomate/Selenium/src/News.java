import java.util.ArrayList;
import java.util.List;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;


public class News 
{
	public static void main(String[] args)
	{
		System.setProperty("webdriver.chrome.driver", "C:\\Users\\Tudor\\Desktop\\selenium\\chromedriver.exe");
		WebDriver driver=new ChromeDriver();
		
		driver.get("http://fiistudent.ddns.us/users/login/");
		
		driver.findElement(By.name("username")).sendKeys("teodora.calarasu@students.info.uaic.ro");
		driver.findElement(By.name("password")).sendKeys("valoare1");
		driver.findElement(By.xpath("//input[@type='submit']")).click();
		
		driver.get("http://fiistudent.ddns.us");
		driver.findElement(By.xpath("//a[@href='/news/']")).click();
		
		List<WebElement> list=new ArrayList<>();
		list=driver.findElements(By.xpath("//p[@class='top']/a"));
		for(WebElement obj:list)
			System.out.println(obj.getText());

		
		try 
		{
			for(char elem='1';elem<='9';elem++)
				if(elem!='7')
			{
				String xpath="//a[@href='" +elem+ "/']";
				System.out.println(driver.findElement(By.xpath(xpath)).getText());
				driver.findElement(By.xpath(xpath)).click();
				driver.findElement(By.xpath("//a[@class='meniu']")).click();
			}	
			
			
			driver.findElement(By.xpath("//img[@src='/static/plus.png']")).click();
			Thread.sleep(3000);
			
			driver.findElement(By.xpath("//input[@type='text']")).sendKeys("");
			driver.findElement(By.xpath("//textarea[@name='body']")).sendKeys("");
			driver.findElement(By.xpath("//button[@type='submit']")).click();
			
			Thread.sleep(3000);
			
			driver.findElement(By.xpath("//input[@type='text']")).sendKeys("Pun anunt desi nu sunt logat");
			driver.findElement(By.xpath("//textarea[@name='body']")).sendKeys("Acesta este mesajul unui user care nu este autentificat si nici nu are permisiuni");
			driver.findElement(By.xpath("//button[@type='submit']")).click();
			
			Thread.sleep(1000);
			
		} catch (Exception e) 
		{
			System.out.println(e.getMessage());
		}
		
		
		driver.close();
		driver.quit();
	}
}
