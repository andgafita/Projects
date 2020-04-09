import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.Select;

public class Personal 
{
	public static String[] firstNames= {"Tudor", "George", "Maria", "Dragos"};

	public static void main(String[] args) throws InterruptedException
	{
		System.setProperty("webdriver.chrome.driver", "C:\\Users\\Tudor\\Desktop\\selenium\\chromedriver.exe");
		WebDriver driver=new ChromeDriver();
		
		driver.get("http://fiistudent.ddns.us/users/login/");
		
		driver.findElement(By.name("username")).sendKeys("teodora.calarasu@students.info.uaic.ro");
		driver.findElement(By.name("password")).sendKeys("valoare1");
		driver.findElement(By.xpath("//input[@type='submit']")).click();
		
		driver.get("http://fiistudent.ddns.us");
		driver.findElement(By.xpath("//a[@href='/users/settings/']")).click();
		
		
		for (String firstName : firstNames) 
		{
			driver.findElement(By.name("last_name")).sendKeys(firstName);

			for (int i = 1; i <= 1; i++) 
			{
				Select category = new Select(driver.findElement(By.name("an_studiu")));
				category.selectByIndex(i);
				for(int j=1;j<=1;j++)
				{
					Select category2 = new Select(driver.findElement(By.name("grupa")));
					category2.selectByIndex(j);
					for(int k=1;k<=1;k++)
					{
						Select category3 = new Select(driver.findElement(By.name("grupa")));
						category3.selectByIndex(k);
						for(int d=1;d<=4;d++)
						{
							Select category4 = new Select(driver.findElement(By.name("color1_first")));
							category4.selectByIndex(d);	
							for(int s=1;s<=4;s++)
							{
								Select category5 = new Select(driver.findElement(By.name("color2_first")));
								category5.selectByIndex(s);		
								for(int l=1;l<=3;l++)
								{
									Select category6 = new Select(driver.findElement(By.name("background_first")));
									category6.selectByIndex(l);	
									for(int u=0;u<=1;u++)
									{
										Select category7 = new Select(driver.findElement(By.name("navbar_color")));
										category7.selectByIndex(u);	
										for(int h=0;h<=4;h++)
										{
											Select category8 = new Select(driver.findElement(By.name("font_family")));
											category8.selectByIndex(h);	
											driver.findElement(By.xpath("//button[@type=\"submit\"]")).click();
										}
									}
								}
							}
						}
					}
				}
			}
		}
		
		driver.close();
		driver.quit();
		
	}
}
