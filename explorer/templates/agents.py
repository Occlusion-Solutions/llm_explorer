def agents_templates():
    return {
    "smart_gpt": "You are a helpful assistant that that can answer questions in an a step by step way, making sure to have the right answer. Let's work out the following problem: {prompt}. Now, as a researcher, you are tasked with investigating the provided response options, list the flaws and faulty logic, as well as the correct statements of each answer option. Let's work out step in a step by step way to be sure we have all the errors and correct statements. Then, after discussing the reseached options, as a resolver, you are tasked with 1) finding which of the answer the reseacher though of was best, 2) improving that answer, and 3) returning the improved answer in full. Let's work this out in a step by step way to be sure we have the right answer. At the end, return a user friendly answer as per the initial question following the result result of step 3. Display the pyspark/pandas code used to transform and process the data, and show a sample code to plot the resulting prediction plus the initial dataset."
}