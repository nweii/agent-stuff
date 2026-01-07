// ABOUTME: Example of a Raycast Form with validation using the useForm hook.
// ABOUTME: Demonstrates TextField, PasswordField, DatePicker, Dropdown, and TagPicker.

import { Action, ActionPanel, Form, showToast, Toast } from "@raycast/api";
import { useForm, FormValidation } from "@raycast/utils";

interface SignUpFormValues {
  firstName: string;
  lastName: string;
  email: string;
  birthday: Date | null;
  password: string;
  role: string;
  interests: string[];
}

export default function Command() {
  const { handleSubmit, itemProps, reset } = useForm<SignUpFormValues>({
    onSubmit(values) {
      showToast({
        style: Toast.Style.Success,
        title: "Account Created!",
        message: `Welcome, ${values.firstName} ${values.lastName}`,
      });
      console.log("Form values:", values);
    },
    initialValues: {
      role: "user",
      interests: [],
    },
    validation: {
      firstName: FormValidation.Required,
      lastName: FormValidation.Required,
      email: (value) => {
        if (!value) {
          return "Email is required";
        }
        if (!value.includes("@")) {
          return "Please enter a valid email address";
        }
      },
      password: (value) => {
        if (!value) {
          return "Password is required";
        }
        if (value.length < 8) {
          return "Password must be at least 8 characters";
        }
      },
      birthday: (value) => {
        if (!value) {
          return "Birthday is required";
        }
      },
    },
  });

  return (
    <Form
      actions={
        <ActionPanel>
          <Action.SubmitForm title="Create Account" onSubmit={handleSubmit} />
          <Action title="Reset Form" onAction={reset} />
        </ActionPanel>
      }
    >
      <Form.Description text="Create your new account" />

      <Form.TextField
        title="First Name"
        placeholder="Enter your first name"
        {...itemProps.firstName}
      />

      <Form.TextField
        title="Last Name"
        placeholder="Enter your last name"
        {...itemProps.lastName}
      />

      <Form.TextField
        title="Email"
        placeholder="you@example.com"
        {...itemProps.email}
      />

      <Form.PasswordField
        title="Password"
        placeholder="At least 8 characters"
        {...itemProps.password}
      />

      <Form.Separator />

      <Form.DatePicker
        title="Birthday"
        type={Form.DatePicker.Type.Date}
        {...itemProps.birthday}
      />

      <Form.Dropdown title="Role" {...itemProps.role}>
        <Form.Dropdown.Item value="user" title="User" />
        <Form.Dropdown.Item value="admin" title="Administrator" />
        <Form.Dropdown.Item value="developer" title="Developer" />
      </Form.Dropdown>

      <Form.TagPicker title="Interests" {...itemProps.interests}>
        <Form.TagPicker.Item value="coding" title="Coding" />
        <Form.TagPicker.Item value="design" title="Design" />
        <Form.TagPicker.Item value="music" title="Music" />
        <Form.TagPicker.Item value="gaming" title="Gaming" />
        <Form.TagPicker.Item value="sports" title="Sports" />
      </Form.TagPicker>
    </Form>
  );
}
